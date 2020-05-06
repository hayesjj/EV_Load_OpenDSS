"""
UCD MV Network Transformer Declarations

James Hayes Feb 2020

"""

"""
DESCRIPTION
This script creates the OpenDSS commands for creating loads.
"""

import pandas as pd # High level data manipulation

data = pd.read_excel('UCD_Bus_Loads_All.xlsx', index_col=0)


Test_dir = "C:/ucd_model_jh_mar_20/Network_data/Network_model/"

file_dir = Test_dir + "Feeder1/"
open(file_dir+'OpenDSS_Loads.txt', 'w').close()

file_dir = Test_dir + "Feeder2/"
open(file_dir+'OpenDSS_Loads.txt', 'w').close()

file_dir = Test_dir + "Feeder3/"
open(file_dir+'OpenDSS_Loads.txt', 'w').close()

file_dir = Test_dir + "Feeder4/"
open(file_dir+'OpenDSS_Loads.txt', 'w').close()

for i in data.index:
    
    if (data.loc[i, 'Feeder']==1).all():
        string = 'New Load.' + i.lower() + ' Phases=' + str(data.loc[i, 'Phases']) + ' Bus1=' + str(data.loc[i, 'Bus1']) + ' kV=' + str(data.loc[i, 'kV']) + ' Pf=' + str(data.loc[i, 'PF']) + ' Model=' + str(data.loc[i, 'Model']) + ' Daily=' + str(data.loc[i, 'Daily']) + ' Vminpu=' + str(data.loc[i, 'Vminpu']) + ' Vmaxpu=' + str(data.loc[i, 'Vmaxpu'])
        file_dir = Test_dir + "Feeder1/"
        with open(file_dir+'OpenDSS_Loads.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()
       
    if (data.loc[i, 'Feeder']==2).all():
        string = 'New Load.' + i.lower() + ' Phases=' + str(data.loc[i, 'Phases']) + ' Bus1=' + str(data.loc[i, 'Bus1']) + ' kV=' + str(data.loc[i, 'kV'])  + ' Pf=' + str(data.loc[i, 'PF']) + ' Model=' + str(data.loc[i, 'Model']) + ' Daily=' + str(data.loc[i, 'Daily']) + ' Vminpu=' + str(data.loc[i, 'Vminpu']) + ' Vmaxpu=' + str(data.loc[i, 'Vmaxpu'])
        file_dir = Test_dir + "Feeder2/"
        with open(file_dir+'OpenDSS_Loads.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

            
    if (data.loc[i, 'Feeder']==3).all():
        string = 'New Load.' + i.lower() + ' Phases=' + str(data.loc[i, 'Phases']) + ' Bus1=' + str(data.loc[i, 'Bus1']) + ' kV=' + str(data.loc[i, 'kV'])  + ' Pf=' + str(data.loc[i, 'PF']) + ' Model=' + str(data.loc[i, 'Model']) + ' Daily=' + str(data.loc[i, 'Daily']) + ' Vminpu=' + str(data.loc[i, 'Vminpu']) + ' Vmaxpu=' + str(data.loc[i, 'Vmaxpu'])
        file_dir = Test_dir + "Feeder3/"
        with open(file_dir+'OpenDSS_Loads.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

    if (data.loc[i, 'Feeder']==4).all():
        string = 'New Load.' + i.lower() + ' Phases=' + str(data.loc[i, 'Phases']) + ' Bus1=' + str(data.loc[i, 'Bus1']) + ' kV=' + str(data.loc[i, 'kV'])  + ' Pf=' + str(data.loc[i, 'PF']) + ' Model=' + str(data.loc[i, 'Model']) + ' Daily=' + str(data.loc[i, 'Daily']) + ' Vminpu=' + str(data.loc[i, 'Vminpu']) + ' Vmaxpu=' + str(data.loc[i, 'Vmaxpu'])
        file_dir = Test_dir + "Feeder4/"
        with open(file_dir+'OpenDSS_Loads.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

            
    