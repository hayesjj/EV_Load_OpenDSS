"""
#### OPF for unbalance three-phase network from OpenDSS ####
#### Valentin Rigoni and Andrew Keane ######################
#### University College Dublin, Ireland ####################
#### email: valentinrigoni09@gmail.com #####################
####        andrew.keane@ucd.ie        #####################

Contributions:
    This model available for anyone to use.
    If you use the model, get in touch and let us know about your work.

Citation:
    When using this model and any of the provided functions and modified network models, please cite our paper which describes them: 
    V. Rigoni and A. Keane, "An Open-Source Optimal Power Flow Formulation: Integrating Pyomo & OpenDSS in Python", 2020 IEEE Power and Energy Society General Meeting, 2020.
"""

def Operation_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Time_sim,Feeder_names,Bus_set_no_slack,DSS_Bus_Vmag,Lines_set,Line_data_DSS,DSS_Imag_line,DSS_P_line,DSS_Q_line,Cable_data,Feeder_bus_validation,Feeder_Lines_validation,DSSMon_Bus_Vmag):
    
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams["font.family"] = "Times New Roman"
    color_phases = ['r','b','m']
    
    ############### Medium Voltage ###############
    Vnom=10000/math.sqrt(3)
    for i_feeder in Feeder_names:
        bus_plot = Feeder_bus_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OpenDSS
            ax.plot(Time_sim/60.0,DSS_Bus_Vmag[np.where(Bus_set_no_slack == bus_plot)[0][0],phase-1,:]/Vnom,'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Bus ' + bus_plot + ' voltage [pu]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        plt.show()
        #fig.savefig(Main_Results_path + '/Validation_Voltages_' + bus_plot + '.png')
        

    ############### Current ###############   
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OpenDSS
            ax.plot(Time_sim/60.0,DSS_Imag_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' current flow [A]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #plt.show()
        #fig.savefig(Main_Results_path + '/Validation_Currents_' + line_plot + '.png')
        
    ############### P flow ###############
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OpenDSS
            ax.plot(Time_sim/60.0,3*DSS_P_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' P flow [kW]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        #plt.show()
        #fig.savefig(Main_Results_path + '/Validation_Pflow_' + line_plot + '.png')
    
    
    ############### Q flow ###############
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OpenDSS
            ax.plot(Time_sim/60.0,3*DSS_Q_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' Q flow [kvar]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        #plt.show()
        #fig.savefig(Main_Results_path + '/Validation_Qflow_' + line_plot + '.png')
    
