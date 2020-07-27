# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 12:47:22 2020

@author: loren
"""


import pandas as pd
import numpy as np

EE_demand = pd.DataFrame()
TH_demand = pd.DataFrame()

min_december = 1440*31
 
#%% Concatenating from December to November 
for i in range(1,5):
    EE_demand = pd.concat([EE_demand, pd.read_csv("RAMP/output_file_"+str(i)+".csv",header=0,index_col=0)], axis=0, ignore_index=True)   
for i in range(5,9):
    TH_demand = pd.concat([TH_demand, pd.read_csv("RAMP/output_file_"+str(i)+".csv",header=0,index_col=0)], axis=1, ignore_index=True)
   
#%% Appending December as last month and dropping from first position  
EE_demand = pd.concat([EE_demand, EE_demand.iloc[0:min_december,:]], axis=0, ignore_index=True)
EE_demand = EE_demand.drop(EE_demand.index[0:min_december])
TH_demand = pd.concat([TH_demand, TH_demand.iloc[0:min_december,:]], axis=0, ignore_index=True)
TH_demand = TH_demand.drop(TH_demand.index[0:min_december])

#%% Reindexing from 1 to 525600 
EE_demand.index = np.arange(1,EE_demand.shape[0]+1)
TH_demand.index = np.arange(1,TH_demand.shape[0]+1)

#%% Exporting
EE_demand.to_csv('Electric_Demand.csv')
TH_demand.to_csv('Thermal_Demand.csv')
