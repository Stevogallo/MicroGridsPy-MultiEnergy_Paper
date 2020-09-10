"""
Multi-Energy System (MESpy) model

Modelling framework for optimization of hybrid electric and thermal small-scale energy systems sizing

Authors: 
    Lorenzo Rinaldi   - Department of Energy, Politecnico di Milano, Milan, Italy
    Stefano Pistolese - Department of Energy, Politecnico di Milano, Milan, Italy
    Nicolò Stevanato  - Department of Energy, Politecnico di Milano, Milan, Italy
                        Fondazione Eni Enrico Mattei, Milan, Italy
    Sergio Balderrama - Department of Mechanical and Aerospace Engineering, University of Liège, Liège, Belgium
                        San Simon University, Centro Universitario de Investigacion en Energia, Cochabamba, Bolivia
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
    
import warnings
warnings.filterwarnings("ignore")


"Import params"
StartDate = '01/07/2017 00:00:00' 
PlotScenario  = 1    
PlotResolution = 1000   
nS = 1
nC = 4
fontticks = 18
fonttitles = 22
fontaxis = 20
fontlegend = 20

idx = pd.IndexSlice

Electric_Energy_Demand = pd.read_csv('a_Traditional-Energy-System/Inputs/Electric_Demand.csv', sep=';', index_col=0) # Import electricity demand
Electric_Energy_Demand = Electric_Energy_Demand.round(3)
Thermal_Energy_Demand = pd.read_csv('a_Traditional-Energy-System/Inputs/Thermal_Demand.csv', sep=';',  index_col=0) # Import thermal energy demand
Thermal_Energy_Demand = Thermal_Energy_Demand.round(3)
    
Electric_Energy_Demand.index = pd.DatetimeIndex(start=StartDate, periods=525600, freq='1min')
Thermal_Energy_Demand.index = pd.DatetimeIndex(start=StartDate, periods=525600, freq='1min')

StartDatePlot = ['12/23/2017 00:00:00','03/23/2017 00:00:00','06/23/2017 00:00:00','09/23/2017 00:00:00'] # MM/DD/YY
EndDatePlot   = ['12/23/2017 23:59:59','03/23/2017 23:59:59','06/23/2017 23:59:59','09/23/2017 23:59:59']

y_Plot1 = Electric_Energy_Demand.loc[StartDatePlot[0]:EndDatePlot[0], :].values
y_Plot2 = Electric_Energy_Demand.loc[StartDatePlot[1]:EndDatePlot[1], :].values
y_Plot3 = Electric_Energy_Demand.loc[StartDatePlot[2]:EndDatePlot[2], :].values
y_Plot4 = Electric_Energy_Demand.loc[StartDatePlot[3]:EndDatePlot[3], :].values
x_Plot  = np.arange(len(y_Plot1))


"Plot"
fig = plt.figure(figsize=(20,20))

#%% Electric load curve
ax1 = plt.subplot2grid((3,2),(0,0),colspan=2)

ax1.plot(x_Plot, y_Plot4, '#2e279d', label='Spring')
ax1.plot(x_Plot, y_Plot1, '#4d80e4', label='Summer')
ax1.plot(x_Plot, y_Plot2, '#46b3e6', label='Fall')
ax1.plot(x_Plot, y_Plot3, '#dff6f0', label='Winter')

ax1.set_xlabel('Time (Hours)', fontsize=fontaxis)
ax1.set_xlim(xmin=0)
ax1.set_xlim(xmax=60*24+1)
ax1.set_xticks([0,(4*60),(8*60),(60*12),(60*16),(60*20),(60*24)])
ax1.set_xticklabels([0,4,8,12,16,20,24], fontsize=fontticks)
ax1.margins(x=0)

ax1.set_ylabel('Power (kW)', fontsize=fontaxis)
ax1.set_ylim(ymin=0)
ax1.set_ylim(ymax=200)
ax1.set_yticks(np.arange(0,201,50))
ax1.set_yticklabels(np.arange(0,201,50), fontsize=fontticks)
ax1.margins(y=0)

ax1.grid(True)
ax1.legend(loc='upper left', fontsize=fontlegend, facecolor='white')

#%% Thermal load curve

subplot_rows = [1,1,2,2]
subplot_cols = [0,1,0,1]

ymax = [350,1200,100,100]

i = 0
for c in Thermal_Energy_Demand.columns:
    y_Plot1 = Thermal_Energy_Demand.loc[StartDatePlot[0]:EndDatePlot[0], c].values
    y_Plot2 = Thermal_Energy_Demand.loc[StartDatePlot[1]:EndDatePlot[1], c].values
    y_Plot3 = Thermal_Energy_Demand.loc[StartDatePlot[2]:EndDatePlot[2], c].values
    y_Plot4 = Thermal_Energy_Demand.loc[StartDatePlot[3]:EndDatePlot[3], c].values
    x_Plot  = np.arange(len(y_Plot1))

    axs = plt.subplot2grid((3,2),(subplot_rows[i],subplot_cols[i]),colspan=1)
    
    axs.plot(x_Plot, y_Plot4, '#8fcfd1', label='Spring')
    axs.plot(x_Plot, y_Plot1, '#df5e88', label='Summer')
    axs.plot(x_Plot, y_Plot2, '#f6ab6c', label='Fall')
    axs.plot(x_Plot, y_Plot3, '#f6efa6', label='Winter')

    if i==0 or i ==2:
        axs.set_ylabel('Power (kW)', fontsize=fontaxis)
    if i==2 or i ==3:
        axs.set_xlabel('Time (Hours)', fontsize=fontaxis)
    
    for tick in axs.yaxis.get_major_ticks():
        tick.label.set_fontsize(fontaxis)
        
    axs.set_ylim(ymin=0)
    axs.set_ylim(ymax=ymax[i])

    axs.margins(x=0)
    axs.margins(y=0)
            
    axs.set_xlim(xmin=0)
    axs.set_xlim(xmax=60*24+1)
    axs.set_xticks([0,(4*60),(8*60),(60*12),(60*16),(60*20),(60*24)])
    axs.set_xticklabels([0,4,8,12,16,20,24], fontsize=fontticks)
    axs.margins(x=0)
    
    if i==0:
        axs.set_title('Commercial activities', fontsize=fonttitles)
    if i==1:
        axs.set_title('Domestic', fontsize=fonttitles)
    if i==2:
        axs.set_title('Public offices', fontsize=fonttitles)
    if i==3:
        axs.set_title('School', fontsize=fonttitles)

    axs.grid(True)
    
    if i==0:
        axs.legend(loc='upper left', fontsize=fontlegend, facecolor='white')
    
    i += 1

fig.tight_layout()    

pylab.savefig('LoadCurves_EE+Th.svg', format='svg')
