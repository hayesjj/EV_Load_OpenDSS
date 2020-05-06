"""
UCD MV Network Transformer Declarations

James Hayes Feb 2020

"""

"""
DESCRIPTION
This script creates the OpenDSS commands for creating the different transformers using the UCD_transformers.xlsx file
"""

import pandas as pd # High level data manipulation

data = pd.read_excel('UCD_transformers.xlsx', index_col=0)


Test_dir = "C:/ucd_model_jh_mar_20/Network_data/Network_model/"

'''Overwriting Existing Commands'''

file_dir = Test_dir + "Feeder1/"
open(file_dir+'OpenDSS_Transformer.txt', 'w').close()

file_dir = Test_dir + "Feeder2/"
open(file_dir+'OpenDSS_Transformer.txt', 'w').close()

file_dir = Test_dir + "Feeder3/"
open(file_dir+'OpenDSS_Transformer.txt', 'w').close()

file_dir = Test_dir + "Feeder4/"
open(file_dir+'OpenDSS_Transformer.txt', 'w').close()

for i in data.index:
    
    if data.loc[i, 'Feeder']==1:
        string = 'New Transformer.' + i + ' phases=' + str(data.loc[i, 'phases']) + ' windings=' + str(data.loc[i, 'windings']) + ' Tap=' + str(data.loc[i, 'Tap']) + ' Buses=[' + str(data.loc[i, 'Bus1'])+' '+ str(data.loc[i, 'Bus2'])+'] Conns=[' + str(data.loc[i, 'Conns'])+'] kVs=[' + str(data.loc[i, 'kVs'])+'] kVAs=[' + str(data.loc[i, 'kVAs'])+'] %Rs=[' + str(data.loc[i, '%Rs'])+'] rneut=' + str(data.loc[i, 'rneut'])+' XHL=' + str(data.loc[i, 'XHL'])+' %loadloss=' + str(data.loc[i, '%loadloss'])+' %noloadloss=' + str(data.loc[i, '%noloadloss'])+' %imag=' + str(data.loc[i, '%imag'])#+' NormHKVA=' + str(data.loc[i, 'NormHKVA'])+' EmergHKVA=' + str(data.loc[i, 'EmergHKVA'])
        file_dir = Test_dir + "Feeder1/"
        with open(file_dir+'OpenDSS_Transformer.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()
       
    if data.loc[i, 'Feeder']==2:
        string = 'New Transformer.' + i + ' phases=' + str(data.loc[i, 'phases']) + ' windings=' + str(data.loc[i, 'windings']) + ' Tap=' + str(data.loc[i, 'Tap']) + ' Buses=[' + str(data.loc[i, 'Bus1'])+' '+ str(data.loc[i, 'Bus2'])+'] Conns=[' + str(data.loc[i, 'Conns'])+'] kVs=[' + str(data.loc[i, 'kVs'])+'] kVAs=[' + str(data.loc[i, 'kVAs'])+'] %Rs=[' + str(data.loc[i, '%Rs'])+'] rneut=' + str(data.loc[i, 'rneut'])+' XHL=' + str(data.loc[i, 'XHL'])+' %loadloss=' + str(data.loc[i, '%loadloss'])+' %noloadloss=' + str(data.loc[i, '%noloadloss'])+' %imag=' + str(data.loc[i, '%imag'])#+' NormHKVA=' + str(data.loc[i, 'NormHKVA'])+' EmergHKVA=' + str(data.loc[i, 'EmergHKVA'])
        file_dir = Test_dir + "Feeder2/"
        with open(file_dir+'OpenDSS_Transformer.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

            
    if data.loc[i, 'Feeder']==3:
        string = 'New Transformer.' + i + ' phases=' + str(data.loc[i, 'phases']) + ' windings=' + str(data.loc[i, 'windings']) + ' Tap=' + str(data.loc[i, 'Tap']) + ' Buses=[' + str(data.loc[i, 'Bus1'])+' '+ str(data.loc[i, 'Bus2'])+'] Conns=[' + str(data.loc[i, 'Conns'])+'] kVs=[' + str(data.loc[i, 'kVs'])+'] kVAs=[' + str(data.loc[i, 'kVAs'])+'] %Rs=[' + str(data.loc[i, '%Rs'])+'] rneut=' + str(data.loc[i, 'rneut'])+' XHL=' + str(data.loc[i, 'XHL'])+' %loadloss=' + str(data.loc[i, '%loadloss'])+' %noloadloss=' + str(data.loc[i, '%noloadloss'])+' %imag=' + str(data.loc[i, '%imag'])#+' NormHKVA=' + str(data.loc[i, 'NormHKVA'])+' EmergHKVA=' + str(data.loc[i, 'EmergHKVA'])
        file_dir = Test_dir + "Feeder3/"
        with open(file_dir+'OpenDSS_Transformer.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

    if data.loc[i, 'Feeder']==4:
        string = 'New Transformer.' + i + ' phases=' + str(data.loc[i, 'phases']) + ' windings=' + str(data.loc[i, 'windings']) + ' Tap=' + str(data.loc[i, 'Tap']) + ' Buses=[' + str(data.loc[i, 'Bus1'])+' '+ str(data.loc[i, 'Bus2'])+'] Conns=[' + str(data.loc[i, 'Conns'])+'] kVs=[' + str(data.loc[i, 'kVs'])+'] kVAs=[' + str(data.loc[i, 'kVAs'])+'] %Rs=[' + str(data.loc[i, '%Rs'])+'] rneut=' + str(data.loc[i, 'rneut'])+' XHL=' + str(data.loc[i, 'XHL'])+' %loadloss=' + str(data.loc[i, '%loadloss'])+' %noloadloss=' + str(data.loc[i, '%noloadloss'])+' %imag=' + str(data.loc[i, '%imag'])#+' NormHKVA=' + str(data.loc[i, 'NormHKVA'])+' EmergHKVA=' + str(data.loc[i, 'EmergHKVA'])
        file_dir = Test_dir + "Feeder4/"
        with open(file_dir+'OpenDSS_Transformer.txt', 'a') as open_file:
            open_file.write(string + '\n')
            open_file.close()

            
    