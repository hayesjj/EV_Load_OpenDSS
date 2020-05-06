"""
Plots the Results for Bus Volatges for Monte Carlo Analysis
"""

def Monte_Carlo_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Time_sim,Feeder_names,Bus_set_mv,Bus_Vmag,Imag_line,Lines_set,Line_data_DSS,Cable_data,Feeder_bus_validation,Feeder_Lines_validation,Pen):
    
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams["font.family"] = "Times New Roman"
    
    ############### Medium Voltage ###############
    Vnom=10000/math.sqrt(3)
    for i_feeder in Feeder_names:
        bus_plot = Feeder_bus_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        
        ax.plot(Time_sim/60.0,Bus_Vmag[np.where(Bus_set_mv == bus_plot)[0][0],:,:]/Vnom,linestyle='-',linewidth=1,alpha=3)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Bus ' + bus_plot + ' voltage [pu]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        #plt.show()
        fig.savefig('C:/Users/'+str(Pen*100)+'% Validation_Voltages_' + bus_plot + '.png')
        

    ############### Current ###############   
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        
        ax.plot(Time_sim/60.0,Imag_line[np.where(Lines_set == line_plot)[0][0],:,:],linestyle='-',linewidth=1,alpha=3)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' current flow [A]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #plt.show()
        fig.savefig('C:/Users/'+str(Pen*100)+'% Validation_Currents_' + line_plot + '.png')
        
    
