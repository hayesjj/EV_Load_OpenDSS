"""
Function to Generate Probalistic Load Profile for a Given Number of Charge Events


Created on Tue Mar 24 12:26:46 2020

@author: James Hayes
"""
import random
import numpy as np
import pandas as pd
from scipy.stats import rv_discrete
import matplotlib.pyplot as plt

# Simulation time
Time_sim_interval = 15 # [5-1440] - Provided profile has a 15 min resolution
Time_start = 15
       # First time step >=5
Time_end = 1440      # Last time step <=1440

""" Aux functions """
def range1(start, end, step): # like range but inlcuding the ending value
    return range(start, end+1, step)
Time_sim = np.array(range1(Time_start,Time_end,Time_sim_interval)) # Time set for simulations
Npts=Time_sim.size

def ev_charger_load(No_evs,bus,Prof_plot):
    p_ev=np.zeros(np.shape(Time_sim))
    p_ev_all=np.zeros([Time_sim.size,No_evs])

    #Load in EV Data for Ireland
    ev_data = pd.read_excel('Irish_ev_data.xlsx')
    
    #Extract Name & Probability
    ev_name = ev_data['Model']
    prob_ev = ev_data['Probability']
    ev = ev_data.index
    
    #Create Distribution for Car Type
    ev_custm = rv_discrete(name='custm', values=(ev, prob_ev))
    ev_distrib = np.array(ev_custm.rvs(size=100))
        
    #Load in SOC Data for Ireland
    soc_data = pd.read_excel('Irish_soc_data.xlsx')
    
    #Extract SOC & Probability
    ev_soc = soc_data['SOC']
    prob_soc = soc_data['Probability']
    soc = ev_data.index
    
    #Create Distribution
    soc_custm = rv_discrete(name='custm', values=(soc, prob_soc))
    soc_distrib = np.array(soc_custm.rvs(size=100))
    
    #Normal Distribution for Arrival Times with mu = 9:00am
    mu, sigma = 510, 60 # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)
    
    for v in range(No_evs):
        
        #Randomly Sample Array and Return Car & SOC
        random_ev = random.choice(ev_distrib)
        ev_to_charge = ev_data.loc[random_ev, ['Battery Size', 'AC Charger', 'DC Charger', 'Type']]
        
        random_soc = random.choice(soc_distrib)
        soc_to_apply = soc_data.loc[random_soc, ['SOC']]
        
        time_start = random.choice(s)
        
        #Create Load Value for Each Timestep for One Vehicle
        for t,j in enumerate(Time_sim):
            time_100 = Time_sim_interval*(ev_to_charge['Battery Size']/ev_to_charge['AC Charger'])
            time_80 = 0.8*time_100
            time_to_charge = time_100*soc_to_apply
            time_end = time_to_charge + time_start
            time_end=int(time_end)
        
            if time_start > Time_sim[t]:
                p_ev[t]=0+ p_ev[t]
                p_ev_all[t,v]=0
            
            elif time_start<=Time_sim[t] and Time_sim[t]<=time_start+time_80:
                p_ev[t]=ev_to_charge['AC Charger']+ p_ev[t]
                p_ev_all[t,v]=ev_to_charge['AC Charger']
            
            elif Time_sim[t] <= time_end:
                p_ev[t]= Time_sim[t]*(ev_to_charge['AC Charger'] /(time_100 - time_80)/60)+ p_ev[t]
                p_ev_all[t,v]=Time_sim[t]*(ev_to_charge['AC Charger'] /(time_100 - time_80)/60)
            else:
                p_ev[t]=0+ p_ev[t]
                p_ev_all[t,v]=0

    if Prof_plot=='y':         
        plt.rcParams.update({'font.size': 11})
        plt.rcParams['figure.dpi'] = 400
        plt.rcParams["font.family"] = "Times New Roman"
        plt.xlim(0,24)
        plt.xticks(range(0,24+2,2))
        plt.plot(Time_sim/60,p_ev_all,linestyle='dashed')
        line2,=plt.plot(Time_sim/60,p_ev,label='Aggregate Load Profile',linestyle='dashdot',color='k')
        #plt.legend(line2)
        plt.xlabel('Time [h]')
        plt.ylabel('Power [kW]')
        plt.title(bus + ' - EV Load Profile')
        plt.show()
                
    return(p_ev,p_ev_all)

                
   

