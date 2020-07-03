#Calculation of T Groundwater as Function of T Amb

import pandas as pd
import math

T_amb = pd.read_csv('TimeSeries/daily_T.csv')
Day_min = T_amb.idxmin().values[0]+1
T_amb_average = T_amb.mean(axis=0)

T_gw = pd.DataFrame(columns=['T_groundwater'])

for d in range(len(T_amb)):
    T_gw.loc[d] = T_amb_average[0] - 3*math.cos(2*math.pi/365*(d+1-Day_min))

P_shower = pd.DataFrame(columns=['P_shower'])
P_handwash = pd.DataFrame(columns=['P_handwash'])
P_cooking = pd.DataFrame(columns=['P_cooking'])


for d in range(len(T_gw)):
    P_shower.loc[d] = 10/60*4186*(40 - T_gw.loc[d].values[0])
    P_handwash.loc[d] = 5/60*4186*(40 - T_gw.loc[d].values[0])
    P_cooking.loc[d] = 5/60*4186*(50 - T_gw.loc[d].values[0])

P_shower.to_csv('P_Shower.csv')
P_handwash.to_csv('P_Handwash.csv')
P_cooking.to_csv('P_Cooking.csv')