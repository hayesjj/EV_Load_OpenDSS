"""
#### Valentin Rigoni and Andrew Keane ######################
#### University College Dublin, Ireland ####################
#### email: valentinrigoni09@gmail.com #####################
"""

def Extract_data_OpenDSS(math,np,pd,dssCircuit,dssText):
    dssElem = dssCircuit.ActiveCktElement
    dssBus = dssCircuit.ActiveBus 
    
    Lines_set = np.array(dssCircuit.Lines.AllNames)
    Bus_set = np.array(dssCircuit.AllBusNames)
    Nodes_set = np.array(dssCircuit.AllNodeNames)
    Trafo_name=np.array(dssCircuit.Transformers.AllNames)
    Trafo_kva=np.zeros([Trafo_name.size])
    
    # Get Transformer Data
    for i, i_trafo in enumerate(Trafo_name): # Loop thought all loads in the system
        dssCircuit.SetActiveElement("Transformer.{}".format(i_trafo)) # Defines the active circuit element. Allows to access some properties
        dssCircuit.Transformers.Name = i_trafo
        Trafo_kva[i]=dssCircuit.Transformers.kva

    # Get buses nominal voltages
    Bus_Vnom = pd.DataFrame(0,index=Bus_set,columns=['Vnom_pp','Vnom_pn'])
    for i, i_bus in enumerate(Bus_set):
        if Bus_set[i].find("lv")!=-1:
            dssCircuit.SetActiveBus(i_bus)
            dssText.Command ='setkvbase Bus=' + str(i_bus) + ' kVLL=0.394 kVLN=0.227'
            Bus_Vnom.loc[i_bus,'Vnom_pp'] = dssBus.kVBase*1000*math.sqrt(3)
            Bus_Vnom.loc[i_bus,'Vnom_pn'] = dssBus.kVBase*1000
        else:
            dssCircuit.SetActiveBus(i_bus)
            dssText.Command ='setkvbase Bus=' + str(i_bus) + ' kVLL=10 kVLN=220'
            Bus_Vnom.loc[i_bus,'Vnom_pp'] = dssBus.kVBase*1000*math.sqrt(3)
            Bus_Vnom.loc[i_bus,'Vnom_pn'] = dssBus.kVBase*1000

    # Get line data
    Line_data_DSS = pd.DataFrame(index=Lines_set, columns=['Sending bus','Receiving bus','Cable code','Length'])
    for i_line in Lines_set:   
        dssCircuit.Lines.Name = i_line
        Line_data_DSS.loc[i_line,'Sending bus']=dssCircuit.Lines.Bus1
        Line_data_DSS.loc[i_line,'Receiving bus']=dssCircuit.Lines.Bus2
        Line_data_DSS.loc[i_line,'Cable code']=dssCircuit.Lines.LineCode
        Line_data_DSS.loc[i_line,'Length']=dssCircuit.Lines.Length

         
    # Get load data
    Loads_set = np.array(dssCircuit.Loads.AllNames)   
    Load_phase = pd.DataFrame(0,index=Loads_set, columns=["phase"]) 
    Load_bus = pd.DataFrame(index=Loads_set, columns=["Bus"]) # you cannot mix string with floats
    Load_Vnom = pd.DataFrame(index=Loads_set, columns=["Vnom [V]"]) # you cannot mix string with floats
    for i_load in Loads_set: # Loop thought all loads in the system
        dssCircuit.SetActiveElement("Load." + i_load) # Defines the active circuit element. Allows to access some properties
        dssCircuit.Loads.Name = i_load
        
        phases = dssElem.NumPhases # Number of phases for this load
        if phases!=3:
            raise ValueError('not three phase load')
        
        dssCircuit.Loads.Name =  i_load # Active load element in dss
        # Get connection phases
        BusNames = dssElem.BusNames[0] # Get the bus connection of this load
        Load_bus.loc[i_load]["Bus"] = BusNames.partition(".")[0]
        Phases_name = BusNames.partition(".")[2]
        #Load_phase.loc[i_load]["phase"] = int(Phases_name) not required for three phase connection
        Load_Vnom.loc[i_load]["Vnom [V]"] = dssCircuit.Loads.kV * 1000
      
    return [Lines_set,Line_data_DSS,Bus_set,Bus_Vnom,Nodes_set,Loads_set,Load_bus,Load_Vnom,Trafo_kva, Trafo_name]
