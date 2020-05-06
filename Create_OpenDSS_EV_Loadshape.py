"""
UCD MV Network Load Declarations

James Hayes Nov 2019

"""
DESCRIPTION
This script creates the OpenDSS commands for creating the different line types using the UCD_load_data.xlsx file
"""

import pandas as pd # High level data manipulation

load_data = pd.read_excel('0_profiles_info.xlsx', index_col=0)

file_dir='C:/ucd_model_jh_mar_20/Network_data/Profiles/Load_profiles'

open('OpenDSS_Loadshapes.txt', 'w').close()
for i in load_data.index:
    string = 'New LoadShape.' + i.lower() + ' Npts=' + str(load_data.loc[i, 'Npts']) + ' csvfile=' + str(load_data.loc[i, 'csvfile']) + '.txt useactual=' + str(load_data.loc[i, 'useactual'])
    open(str(load_data.loc[i, 'csvfile'])+'.txt', 'w').close()
    with open('OpenDSS_Loadshapes.txt', 'a') as open_file:
     open_file.write(string + '\n')

