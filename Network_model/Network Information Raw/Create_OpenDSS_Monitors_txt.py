"""
UCD MV Network Monitor Declarations

James Hayes Dec 2019

Citation:
    When using this model and any of the provided functions and modified network models, please cite our paper which describes them: 
    V. Rigoni and A. Keane, "A publicly available unbalanced optimal power flow: integrating Pyomo-OpenDSS in Python", 2020 IEEE Power and Energy Society General Meeting, 2020.
"""

"""
DESCRIPTION
This script creates the OpenDSS commands for creating the different monitors using the UCD_mv_monitors.xlsx file
"""

import pandas as pd # High level data manipulation

data = pd.read_excel('UCD_Monitors_All.xlsx', index_col=0)

Test_dir = "C:/ucd_model_jh_jan_20/Network_data/Network_model/"


file_dir = Test_dir + "Feeder1/"
open(file_dir+'OpenDSS_Monitors.txt', 'w').close()

file_dir = Test_dir + "Feeder2/"
open(file_dir+'OpenDSS_Monitors.txt', 'w').close()

file_dir = Test_dir + "Feeder3/"
open(file_dir+'OpenDSS_Monitors.txt', 'w').close()

file_dir = Test_dir + "Feeder4/"
open(file_dir+'OpenDSS_Monitors.txt', 'w').close()

for i in data.index:
    
    if (data.loc[i, 'Feeder']==1).all():
        string = 'New Monitor.' + i + ' Line.' + str(data.loc[i, 'Element']) + ' Terminal=' + str(data.loc[i, 'Terminal']) + ' Mode=' + str(data.loc[i, 'Mode']) + ' ' + str(data.loc[i, 'Polar'])
        file_dir = Test_dir + "Feeder1/"
        with open(file_dir+'OpenDSS_Monitors.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()
       
    if (data.loc[i, 'Feeder']==2).all():
        string = 'New Monitor.' + i + ' Line.' + str(data.loc[i, 'Element']) + ' Terminal=' + str(data.loc[i, 'Terminal']) + ' Mode=' + str(data.loc[i, 'Mode']) + ' ' + str(data.loc[i, 'Polar'])
        file_dir = Test_dir + "Feeder2/"
        with open(file_dir+'OpenDSS_Monitors.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()
     
    if (data.loc[i, 'Feeder']==3).all():
        string = 'New Monitor.' + i + ' Line.' + str(data.loc[i, 'Element']) + ' Terminal=' + str(data.loc[i, 'Terminal']) + ' Mode=' + str(data.loc[i, 'Mode']) + ' ' + str(data.loc[i, 'Polar'])
        file_dir = Test_dir + "Feeder3/"
        with open(file_dir+'OpenDSS_Monitors.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

    if (data.loc[i, 'Feeder']==4).all():
        string = 'New Monitor.' + i + ' Line.' + str(data.loc[i, 'Element']) + ' Terminal=' + str(data.loc[i, 'Terminal']) + ' Mode=' + str(data.loc[i, 'Mode']) + ' ' + str(data.loc[i, 'Polar'])
        file_dir = Test_dir + "Feeder4/"
        with open(file_dir+'OpenDSS_Monitors.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()