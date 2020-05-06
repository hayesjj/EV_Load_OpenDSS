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

def Extract_DSSmonitors_data(np,pd,Npts,dssCircuit,dssMonitors,Buses,Line_data_DSS,Lines_set, Trafo_name):
    # print(Buses)
    # print(Line_data_DSS, Lines_set)
    # print(dssCircuit)
    # print(Npts)

    ## Monitor channels ##    
    # VI monitors
    # V1 deg1 V2 deg2 V3 deg3 I1 degI1 I2 degI2 I3 degI3
    # PQ monitors
    # P1 Q1 P2 Q2 P3 Q3 [kW & kvar]
    
    #Transformer Secondary Voltages
    DSSMon_LVBus_Vmag = np.zeros([Trafo_name.size,3,Npts])
    for i in range(len(Trafo_name)): 
        dssMonitors.Name = Trafo_name[i] + '_lv'
        for phase in range(3):
            DSSMon_LVBus_Vmag[i,phase,:] = dssMonitors.Channel(phase+1)
    
    # Medium Bus Voltages
    DSSMon_Bus_Vmag = np.zeros([Buses.size,3,Npts])
    DSSMon_Bus_Vdeg = np.zeros([Buses.size,3,Npts])
    for i_bus in range(len(Buses)): 
        if Buses[i_bus]=='esb_sub':
            Line = Line_data_DSS.loc[Line_data_DSS['Sending bus']==Buses[i_bus]].index.values[0]  
            dssMonitors.Name = Line + '_vi_sending'
        else:
            Line = Line_data_DSS.loc[Line_data_DSS['Receiving bus']==Buses[i_bus]].index.values[0]
            dssMonitors.Name = Line + '_vi_receiving'
        for phase in range(3):
            DSSMon_Bus_Vmag[i_bus,phase,:] = dssMonitors.Channel((phase)*2+1)
            DSSMon_Bus_Vdeg[i_bus,phase,:] = dssMonitors.Channel((phase)*2+2)
            
    ## Flows from the monitors
    DSSMon_Imag_line = np.zeros([Lines_set.size,3,Npts])
    DSSMon_P_line = np.zeros([Lines_set.size,3,Npts])
    DSSMon_Q_line = np.zeros([Lines_set.size,3,Npts])
    DSSMon_P_Trafo = np.zeros([Lines_set.size,3,Npts])
    DSSMon_Q_Trafo = np.zeros([Lines_set.size,3,Npts])
    DSSMon_I1mag_Trafo = np.zeros([Lines_set.size,3,Npts])
    DSSMon_kVA_Trafo_a = np.zeros([Lines_set.size,Npts])


    for i_line,i in enumerate(Lines_set):
        
        if Lines_set[i_line].find("mv2_")!=-1:
             # Current
            dssMonitors.Name = Lines_set[i_line] + '_vi_receiving'
            for phase in range(3):
                DSSMon_Imag_line[i_line,phase,:] = dssMonitors.Channel((phase)*2+7)
                DSSMon_I1mag_Trafo[i_line,phase,:] = dssMonitors.Channel((phase)*2+7)
            
            # PQ flows
            dssMonitors.Name = Lines_set[i_line] + '_pq_receiving'
            for phase in range(3):
                DSSMon_P_Trafo[i_line,phase,:] = dssMonitors.Channel((phase)*2+1)
                DSSMon_Q_Trafo[i_line,phase,:] = dssMonitors.Channel((phase)*2+2)
                DSSMon_kVA_Trafo_a[i_line,:] = (np.sum(DSSMon_P_Trafo[i_line,:,:],0)**2 + np.sum(DSSMon_Q_Trafo[i_line,:,:],0)**2)**0.5
                DSSMon_kVA_Trafo = pd.DataFrame(DSSMon_kVA_Trafo_a,index=Lines_set[:])

        else:
            # Current
            dssMonitors.Name = Lines_set[i_line] + '_vi_sending'
            for phase in range(3):
                DSSMon_Imag_line[i_line,phase,:] = dssMonitors.Channel((phase)*2+7)
            # PQ flows
            dssMonitors.Name = Lines_set[i_line] + '_pq_sending'
            for phase in range(3):
                DSSMon_P_line[i_line,phase,:] = dssMonitors.Channel((phase)*2+1)
                DSSMon_Q_line[i_line,phase,:] = dssMonitors.Channel((phase)*2+2)
    
    #DSSMon_kVA_Trafo_a=DSSMon_kVA_Trafo_a[~np.all(DSSMon_kVA_Trafo_a == 0, axis=1)]
    DSSMon_kVA_Trafo=DSSMon_kVA_Trafo.loc[~(DSSMon_kVA_Trafo==0).all(axis=1)]

           
    return [DSSMon_Bus_Vmag,DSSMon_Bus_Vdeg,DSSMon_LVBus_Vmag,DSSMon_Imag_line,DSSMon_P_line,DSSMon_Q_line,DSSMon_kVA_Trafo,DSSMon_P_Trafo]