# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Data from Field Campaign Pistolese-Stevanato 2017

Domestic Loads
365 days
'''


from core import User, np, pd
User_list = []


#Create new user classes
Domestic = User("Domestic",332)
User_list.append(Domestic)



#Domestic

Domestic_Dinner_DW = Domestic.Appliance(Domestic,1,pd.read_csv('TimeSeries/P_Cooking.csv'),1,9,0.2,3,thermal_P_var = 0.5, P_series = True)
Domestic_Dinner_DW.windows([1200,1320],[0,0],0.35)

Domestic_Lunch_DW = Domestic.Appliance(Domestic,1,pd.read_csv('TimeSeries/P_Cooking.csv'),1,9,0.2,3,thermal_P_var = 0.5, P_series = True)
Domestic_Lunch_DW.windows([720,900],[0,0],0.35)

Domestic_Shower_wd = Domestic.Appliance(Domestic,1,pd.read_csv('TimeSeries/P_Shower.csv'),2,28,0.2,7,thermal_P_var = 0.5, wd_we_type = 0, P_series = True)
Domestic_Shower_wd.windows([420,540],[1140,1260],0.35)

Domestic_Shower_we = Domestic.Appliance(Domestic,1,pd.read_csv('TimeSeries/P_Shower.csv'),2,28,0.2,7,thermal_P_var = 0.5, wd_we_type = 1, P_series = True)
Domestic_Shower_we.windows([420,1260],[0,0],0.35)

Domestic_HFW = Domestic.Appliance(Domestic,1,pd.read_csv('TimeSeries/P_Handwash.csv'),2,8,0.2,1,thermal_P_var = 0.5, P_series = True)
Domestic_HFW.windows([720,840],[1140,1230],0.35)

Dom_Noise = Domestic.Appliance(Domestic,1,10000, 1, 10, 0.2, 1, thermal_P_var = 0.5)
Dom_Noise.windows([0,1440],[0,0])


