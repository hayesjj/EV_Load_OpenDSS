"""
******************************************************
University College Dublin Medium Voltage Network

January 2020

Author:James Hayes (ME Elec. Energy Eng. Project)

Credit: Valentin Rigoni, Prof. Andrew Keane

******************************************************

Network Description:

The UCD MV system has 4 main feeders. Under normal
operating conditions these are four separate radials
but the facility exists to manually mesh them. The
network radials are at 10kV.

******************************************************
"""

""" Call modules """
# Import all the python and OpenDSS libraries needed for the script
import os
import pandas as pd # High level data manipulation
import numpy as np
import win32com.client # To access the OpenDSS COM module
from win32com.client import makepy
import sys
import math
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook

# Packages
from Main_packages.Extract_OpenDSS_data import Extract_data_OpenDSS
from Main_packages.Plots import Operation_Plots
from Main_packages.Extract_DSSmonitors_data import Extract_DSSmonitors_data
from Main_packages.Assign_EV_Type_SOC import ev_charger_load
from Main_packages.Monte_Carlo_Plots import Monte_Carlo_Plots
"""
******************************************************
                    Folder Paths
******************************************************
"""
# Get directory path
Main_path = os.path.dirname(os.path.realpath(__file__))
Network_model_path = Main_path + '/Network_data/Network_model'
Profiles_path = Main_path + '/Network_data/Profiles'
Main_Results_path = Main_path + '/Main_Results'
"""
******************************************************
                     Inputs
******************************************************
"""
plt.ioff()
show_plots = 'y' # - 'y' or 'n' Plot Line Flows and Bus Voltages
Prof_plot = 'n'  # Plot the Stochastic Load Profile at each bus
Penetration = [0.25, 0.5, 0.75, 1]; # value 0-1 representing percentage EV penetration on UCD Grid at Each Bus
Feeder_names = ['Feeder1','Feeder2','Feeder3','Feeder4'] #Feeders to include in simulation

# Buses and lines to plot
#Plot the First Bus On Each Feeder
Feeder_bus_validation = dict(Feeder1='rosemount_unit_sub', Feeder2='ardmore_sub',Feeder3='arts_sub_tx3', Feeder4='civil_engineering_sub_tx1')

#Plot the Main Line for Each Feeder
Feeder_Lines_validation = {'Feeder1': 'mv1_26','Feeder2': 'mv1_1','Feeder3' : 'mv1_2','Feeder4' : 'mv1_4'}

#Iterations for MonteCarlo
Iterations = 500

#Decalre Arrays for MonteCarlo Results
Bus_Vmag = np.zeros([64, 96, Iterations])
Imag_line = np.zeros([63, 96, Iterations])
Trafo_Loading_All= np.zeros([33,Iterations])

for pen in range(len(Penetration)):
    Pen = Penetration[pen]
    print(Pen)
    for i_iter in range(0,Iterations):
        """
        ******************************************************
                             SCRIPT
        ******************************************************
        """
        print('Iterations remaining:',Iterations-i_iter)
        # Simulation time
        Time_sim_interval = 15 # [5-1440] - Provided profile has a 15 min resolution
        Time_start = 15        # First time step >=5
        Time_end = 1440      # Last time step <=1440
        
        """ Aux functions """
        def range1(start, end, step): # like range but inlcuding the ending value
            return range(start, end+1, step)
        Time_sim = np.array(range1(Time_start,Time_end,Time_sim_interval)) # Time set for simulations
        Npts=Time_sim.size
        
        #Create the OpenDss Circuit
        # Create OpenDSS object
        # The COM module has a variety of interfaces, and creating variables to access them directly is handy.
        sys.argv = ["makepy", "OpenDSSEngine.DSS"]
        makepy.main()
        dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
        dssText = dssObj.Text # to excecute OpenDSS text commands
        dssText.Command = 'Clear' # clear any existing circuit in the engine
        dssCircuit = dssObj.ActiveCircuit # Use it to access the elements in the circuit (e.g., capacitors, buses, etc.)
        dssSolution = dssCircuit.Solution
        dssElem = dssCircuit.ActiveCktElement
        dssBus = dssCircuit.ActiveBus
        
        
        # This is the datapath were the dss file is. Results will also be saved here.
        dssText.Command = 'set datapath=' + Main_path
        dssText.Command ='Set DefaultBaseFrequency=50'
        
        
        # Sets the Reference Bus to be the ESB 38kV Substation & Sets Voltage Base
        dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/OpenDSS_NewCircuit.txt'
        # Line codes
        dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/Cable_data/OpenDSS_line_types.txt'
        #Loadshapes
        dssText.Command = 'Redirect ' + Profiles_path + '/Load_profiles/OpenDSS_Loadshapes.txt'
        #Generators - Currently contains CHP Electricity at Boilerhouse & SLLSC
        dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/Generators/OpenDSS_Generators.txt'
        
        """
        Applying the Stochastic EV Load At Each Bus
        Function called for each 'EV' bus and aggregate load profile returned 
        for specified number of charging events at that bus.
        """
        #Assign the Buses with EVs Attached
        ev_load_bus = pd.read_excel(Main_path + '/Network_data/Network_model/UCD_EV_buses.xlsx',index_col=0)
        ev_load_bus.index = ev_load_bus.index.str.lower()
        
        open(Profiles_path+'/EV_profiles/OpenDSS_EV_Loads.txt', 'w').close()
    
        for i, i_bus in enumerate(ev_load_bus.index):
            if ev_load_bus.loc[i_bus,'EV Status']== 'Y':
                open(Profiles_path+'/EV_profiles/'+i_bus+'_ls_ev.txt', 'w').close()
                [P_ev,P_ev_all] = ev_charger_load(int(round(Pen*ev_load_bus.loc[i_bus,'Max EVs'])),i_bus,Prof_plot)
                
                #Write the OpenDSS Command for Load & LoadShape
                string = 'New LoadShape.'+i_bus+'_ls_ev Npts=96 mInterval=15 csvfile='+i_bus+'_ls_ev.txt useactual=yes'
                string1 ='New Load.' + i_bus + '_ev_l Phases=3 Bus1=' + i_bus + ' kV=0.38 Pf=1 Model=1 Daily='+i_bus+'_ls_ev Vminpu=0.8 Vmaxpu=1.2'
        
                with open(Profiles_path+'/EV_profiles/OpenDSS_EV_Loads.txt', 'a') as open_file:
                    open_file.write(string + '\n' + string1 + '\n')
                       
                for j,i in enumerate(P_ev):
                    string2 = str(P_ev[j])
                    with open(Profiles_path+'/EV_profiles/'+i_bus+'_ls_ev.txt', 'a') as open_file:
                        open_file.write(string2 + '\n')
            else:
                i_bus=i_bus
        
        #EV Loads & Loadshapes
        dssText.Command = 'Redirect ' + Profiles_path + '/EV_profiles/OpenDSS_EV_Loads.txt'
        # Lines, Transformers, Monitors and loads
        for i_feeder in Feeder_names:
            dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Lines.txt'
            dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Transformer.txt'
            dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Loads.txt'
            dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Monitors.txt'
            dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Trafo_Monitors.txt'
        
        dssText.Command = 'set datapath=' + Main_path
        #Solve the Powerflow at Each Interval of the Loadshape & Extract OpenDSS Circuit Data
        dssText.Command ='Reset Monitors'; #Clears the monitors data
        dssText.Command = 'set mode=daily stepsize=15m number=96'
        dssText.Command = 'Set Algorithm=Normal'
        dssSolution.Solve()
        if dssSolution.Converged !=1:
            raise ValueError('Solution did not Converge')
     
        #Function to Extract Network Data From OpenDSS   
        [Lines_set, Line_data_DSS, Bus_set, Bus_Vnom, Nodes_set, Loads_set, Load_bus, Load_Vnom, Trafo_kva, Trafo_name] = Extract_data_OpenDSS(math, np, pd, dssCircuit,dssText)
        
        # Distinguishing between LV and MV Buses Across Campus
        Bus_set_mv = np.array([])
        Bus_set_lv = np.array([])
        
        for i, i_bus in enumerate(Bus_set):
            if Bus_set[i].find("lv")==-1:
                Bus_mv=Bus_set[i]
                Bus_set_mv=np.append(Bus_set_mv, Bus_mv)
            else: 
                Bus_lv=Bus_set[i]
                Bus_set_lv=np.append(Bus_set_lv, Bus_lv)
                
        #Extract DSS Monitors in the Format
        """
        DSSMon_Bus_Vmag = [Bus, Phase, Time]
        DSSMon_Bus_Vdeg = [Bus, Phase, Time]
        DSSMon_LVBus_Vmag = [Bus, Phase, Time]
        DSSMon_Imag_line = [Line, Phase, Time]
        DSSMon_P_line = [Line, Phase, Time]
        DSSMon_Q_line = [Line, Phase, Time]
        """
        dssMonitors = dssCircuit.Monitors
        
        [DSSMon_Bus_Vmag, DSSMon_Bus_Vdeg, DSSMon_LVBus_Vmag, DSSMon_Imag_line, DSSMon_P_line, DSSMon_Q_line,DSSMon_kVA_Trafo,DSSMon_P_Trafo] = Extract_DSSmonitors_data(np,pd,Npts,dssCircuit,dssMonitors,Bus_set_mv,Line_data_DSS,Lines_set, Trafo_name)
        
        #Save the Voltages & Currents for Each Iteration of Monte Carlo Simulation
        Imag_line[:,:,i_iter] = np.vstack(DSSMon_Imag_line[:,1,:])
        Bus_Vmag[:,:,i_iter] = np.vstack(DSSMon_Bus_Vmag[:,1,:])
       
        #Transformer Loading In Each Day During One Iteration of Monte Carlo
        col_list = ["Name", "Rated kVA","feed_line"]
        Trafo_data = pd.read_excel(Main_path + '/Network_data/Network_model/UCD_transformers.xlsx',usecols=col_list,index_col=0)
        
        #Calculate the Max Loading
        Max_Trafo_Load = pd.DataFrame(DSSMon_kVA_Trafo.max(axis=1),columns=['Max Laod kVA'])
        Trafo_Data = pd.merge(Trafo_data, Max_Trafo_Load, left_on="feed_line", right_index=True)
        Trafo_Loading = pd.DataFrame(round((Trafo_Data['Max Laod kVA']/Trafo_Data['Rated kVA'])*100),columns=['% Loading'])
        Trafo_Loading_All[:,i_iter] = Trafo_Loading['% Loading']
        Trafo_Loading = pd.merge(Trafo_data,Trafo_Loading, left_on="Name",right_index=True)
    
        """
        Plot Bus Voltages & Line Powers & Currents
        """
        # Cable type data
        Cable_data = pd.read_excel(Main_path + '/Network_data/Network_model/Cable_data/Cable_data.xlsx',index_col=0 )
        Cable_data.index = Cable_data.index.str.lower()
    
        filelist = [ f for f in os.listdir(Main_Results_path)]
        for f in filelist:
            os.remove(os.path.join(Main_Results_path, f))
                
        if show_plots=='y':
            #Plot and save
            figure_size = (17, 7)
            font_size = 25
            #Operation_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Time_sim,Feeder_names,Bus_set_mv
                          #,DSSMon_Bus_Vmag,Lines_set,Line_data_DSS,DSSMon_Imag_line,DSSMon_P_line,DSSMon_Q_line,Cable_data,Feeder_bus_validation,Feeder_Lines_validation,DSSMon_Bus_Vmag)

    #Transformer Loading
    Max_Trafo_Loading = pd.DataFrame(Trafo_Loading_All.max(axis=1),columns = ['Maximum'],index = Trafo_Data.index)
    Min_Trafo_Loading = pd.DataFrame(Trafo_Loading_All.min(axis=1),columns = ['Minimum'],index = Trafo_Data.index)
    Mean_Trafo_Loading = pd.DataFrame(Trafo_Loading_All.mean(axis=1),columns = ['Mean'],index = Trafo_Data.index)
    Summary_Trafo_Loading = pd.concat([Max_Trafo_Loading,Mean_Trafo_Loading,Min_Trafo_Loading],axis=1)
    
    #Cable Loading
    Cable_Max_Current = pd.DataFrame(pd.read_excel(Main_path + '/Network_data/Network_model/UCD_Lines_All.xlsx',index_col=0),columns=['Current Rating'])
    Max_Cable_Load = pd.DataFrame(Imag_line.max(axis=1).max(axis=1),columns = ['Maximum'],index = Cable_Max_Current.index)
    Min_Cable_Load = pd.DataFrame(Imag_line.min(axis=1).min(axis=1),columns = ['Minimum'],index = Cable_Max_Current.index)
    Mean_Cable_Load = pd.DataFrame(Imag_line.mean(axis=1).min(axis=1),columns = ['Mean'], index = Cable_Max_Current.index)
    Summary_Cable_Load = pd.concat([Max_Cable_Load,Mean_Cable_Load,Min_Cable_Load,Cable_Max_Current],axis=1)
    
    #Bus Voltages
    Max_Bus_Voltage = pd.DataFrame((Bus_Vmag.max(axis=1).max(axis=1))/(10000/np.sqrt(3)),columns = ['Maximum'],index = Bus_set_mv)
    Min_Bus_Voltage = pd.DataFrame((Bus_Vmag.min(axis=1).min(axis=1))/(10000/np.sqrt(3)),columns = ['Minimum'],index = Bus_set_mv)
    Mean_Bus_Voltage = pd.DataFrame((Bus_Vmag.mean(axis=1).mean(axis=1))/(10000/np.sqrt(3)),columns = ['Mean'],index = Bus_set_mv)
    Summary_Bus_Voltage = pd.concat([Max_Bus_Voltage,Mean_Bus_Voltage,Min_Bus_Voltage],axis=1)
    
    with pd.ExcelWriter('C:/Users/temp2015/OneDrive - University College Dublin/5th_Year_Semester_1/EEEN40260_ME_Electrical_Energy_Project/Results/Summary_Results/'+str(Pen*100)+'%Summary.xlsx') as writer:  
        Summary_Trafo_Loading.to_excel(writer, sheet_name='Trafo_Loading')
        Summary_Cable_Load.to_excel(writer, sheet_name='Cable_Loading')
        Summary_Bus_Voltage.to_excel(writer, sheet_name='Bus_Voltages')
    
    Monte_Carlo_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Time_sim,Feeder_names,Bus_set_mv,Bus_Vmag,Imag_line,Lines_set,Line_data_DSS,Cable_data,Feeder_bus_validation,Feeder_Lines_validation,Pen)
        
        
