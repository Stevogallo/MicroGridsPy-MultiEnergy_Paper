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

School = User("school",1)
User_list.append(School)


#Create new appliances


School_Kitchen = School.Appliance(School,2,pd.read_csv('TimeSeries/P_Cooking.csv'),1,90,0.2,1,thermal_P_var = 0.5, wd_we_type = 0, P_series = True)
School_Kitchen.windows([600,960],[0,0],0.35)

School_HFW_1 = School.Appliance(School,5,pd.read_csv('TimeSeries/P_Handwash.csv'),1,20,0,1,thermal_P_var = 0.5, wd_we_type = 0, P_series = True)
School_HFW_1.windows([480,840],[0,0],0.35)

School_HFW_2 = School.Appliance(School,5,pd.read_csv('TimeSeries/P_Handwash.csv'),1,10,0,1,thermal_P_var = 0.5, wd_we_type = 0, P_series = True)
School_HFW_2.windows([840,1080],[0,0],0.35)

School_Noise = School.Appliance(School,1,10000, 1, 15, 0.2, 1, thermal_P_var = 0.5, wd_we_type = 0)
School_Noise.windows([0,1440],[0,0])

