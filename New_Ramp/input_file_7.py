# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Data from Field Campaign Pistolese-Stevanato 2017
'''


from core import User, np, pd
User_list = []


#Create new user classes

Public = User("public",6)
User_list.append(Public)

#Create new appliances

Public_Shower = Public.Appliance(Public,1,pd.read_csv('TimeSeries/P_Shower.csv'),1,20,0.2,5,thermal_P_var = 0.5, P_series = True)
Public_Shower.windows([420,540],[0,0],0.35)

Public_HFW = Public.Appliance(Public,2,pd.read_csv('TimeSeries/P_Handwash.csv'),1,10,0.2,4,thermal_P_var = 0.5, P_series = True)
Public_HFW.windows([420,1200],[0,0],0.35)

Public_FoodUse = Public.Appliance(Public,1,pd.read_csv('TimeSeries/P_Cooking.csv'),2,10,0.2,1,thermal_P_var = 0.5, P_series = True)
Public_FoodUse.windows([720,900],[1140,1320],0.35)

Public_Noise = Public.Appliance(Public,1,10000, 1, 15, 0.2, 1, thermal_P_var = 0.5)
Public_Noise.windows([0,1440],[0,0])


