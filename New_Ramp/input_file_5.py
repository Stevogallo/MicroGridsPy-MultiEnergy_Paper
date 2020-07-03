# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Data from Field Campaign Pistolese-Stevanato 2017

Commercial Activities
365 days
'''



from core import User, np, pd
User_list = []


#Create new user classes

Comm = User("commercialactivities",32)
User_list.append(Comm)


# Commercial Actvities

Comm_standard_use = Comm.Appliance(Comm,1,pd.read_csv('TimeSeries/P_Cooking.csv'),2,240,0.1,10,thermal_P_var = 0.5, P_series = True)
Comm_standard_use.windows([600,900],[1080,1380],0.1)

Comm_Noise = Comm.Appliance(Comm,1,10000, 1, 15, 0.2, 1, thermal_P_var = 0.5)
Comm_Noise.windows([0,1440],[0,0])
