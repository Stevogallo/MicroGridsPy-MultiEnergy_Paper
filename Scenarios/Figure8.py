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
import itertools
    
import warnings
warnings.filterwarnings("ignore")

"Import params"
StartDate = '01/07/2017 00:00:00' 
PlotScenario  = 1    
PlotResolution = 1000 
PlotStartDate = 383040    
PlotEndDate   = 383040+1441      
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

ax1.plot(x_Plot, y_Plot4, '#2e279d', label='_nolegend_')
ax1.plot(x_Plot, y_Plot1, '#4d80e4', label='_nolegend_')
ax1.plot(x_Plot, y_Plot2, '#46b3e6', label='_nolegend_')
ax1.plot(x_Plot, y_Plot3, '#dff6f0', label='_nolegend_')

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


# %% Electric dispatch
configurations = ['a_Traditional-Energy-System',
                  'b_Conventional-MicroGrid',
                  'c_Multi-Good-MicroGrid',
                  'd_Multi-Energy-System']


TimeSeries = {}

subplot_rows = [1,1,2,2]
subplot_cols = [0,1,0,1]

TimeSeries['Th'] = {}

for s in range(1,nS+1):
    TimeSeries['Th']['Sc'+str(s)] = {}
        
    for c in range(nC):
        TimeSeries['Th']['Sc'+str(s)]['Class'+str(c+1)] = pd.read_csv('d_Multi-Energy-System/Results/TimeSeries/Sc'+str(s)+'/Th_TimeSeries_Class'+str(c+1)+'.csv', index_col=[0])
        
        "Series preparation"
        TankNominalCapacity = pd.read_excel('d_Multi-Energy-System/Results/EnergySystemSize.xlsx','Size',index_col=[0,1]).loc[idx['Tank',:],'Class'+str(c+1)].to_frame().iloc[0,0]

        "Series preparation"
        y_SC          = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,2].values
        y_Boiler      = -1*TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,5].values
        y_ElResProd   = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,6].values        
        y_LostLoad    = -1*TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,1].values
        y_Tank_Out    = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,3].values     
        y_Tank_In     = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,3].values             
        y_Demand      = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,0].values
        y_Tank_SOC    = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c+1)].iloc[PlotStartDate:PlotEndDate,-1].values/TankNominalCapacity*100   
        x_Plot = np.arange(len(y_Boiler))
                        
        y_Stacked_1 = [y_Demand,
                       y_Boiler,
                       y_LostLoad]

        y_Stacked_2 = [y_SC,
                       y_ElResProd]

        "Plot"        
        axs = plt.subplot2grid((3,2),(subplot_rows[c],subplot_cols[c]),colspan=1)
        ax2=axs.twinx()
        
        Colors1 = ['#3a86ff',
                  '#8d99ae',
                  '#f72585']

        Colors2 = ['#ffbe0b',
                  '#aacc00']
        
        if c==0:             
            Labels1 = ['Tank',
                      'Boiler',
                      '_nolegend_'] 

            Labels2 = ['Solar collector',
                      'Resistance'] 

            stacks1 = axs.stackplot(x_Plot, y_Stacked_1, labels=Labels1, colors=Colors1, alpha=1, zorder=2)
            stacks2 = axs.stackplot(x_Plot, y_Stacked_2, labels=Labels2, colors=Colors2, alpha=0.5, zorder=2)
            axs.plot(x_Plot, y_Demand, color='black', label='Demand', zorder=2)
            ax2.plot(x_Plot, y_Tank_SOC, '--', color='black', label='_nolegend_', zorder=2)
            
            hatches=["\\", "","",""]
            for stack, hatch in zip(stacks1, hatches):
                stack.set_hatch(hatch)

            
        if c==1:
            Labels1 = ['_nolegend_',
                      '_nolegend_',
                      'Lost load']

            Labels2 = ['_nolegend_',
                      '_nolegend_'] 

            stacks1 = axs.stackplot(x_Plot, y_Stacked_1, labels=Labels1, colors=Colors1, alpha=1, zorder=2)
            stacks2 = axs.stackplot(x_Plot, y_Stacked_2, labels=Labels2, colors=Colors2, alpha=0.5, zorder=2)
            axs.plot(x_Plot, y_Demand, color='black', label='_nolegend_', zorder=2)
            ax2.plot(x_Plot, y_Tank_SOC, '--', color='black', label='Tank state of\ncharge', zorder=2)

            hatches=["\\", "","",""]
            for stack, hatch in zip(stacks1, hatches):
                stack.set_hatch(hatch)

        else:
            Labels1 = ['_nolegend_',
                      '_nolegend_',
                      '_nolegend_']

            Labels2 = ['_nolegend_',
                      '_nolegend_'] 

            stacks1 = axs.stackplot(x_Plot, y_Stacked_1, labels=Labels1, colors=Colors1, alpha=1, zorder=2)
            stacks2 = axs.stackplot(x_Plot, y_Stacked_2, labels=Labels2, colors=Colors2, alpha=0.5, zorder=2)
            axs.plot(x_Plot, y_Demand, color='black', label='_nolegend_', zorder=2)
            ax2.plot(x_Plot, y_Tank_SOC, '--', color='black', label='_nolegend_', zorder=2)

            hatches=["\\", "","",""]
            for stack, hatch in zip(stacks1, hatches):
                stack.set_hatch(hatch)


        if c==0 or c==2:
            axs.set_ylabel('Power (kW)', fontsize=fontaxis)
        if c==2 or c==3:
            axs.set_xlabel('Time (Hours)', fontsize=fontaxis)
        if c==1 or c==3:
            ax2.set_ylabel('State of charge (%)', fontsize=fontaxis)
    
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        ticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = [d*6 for d in range(nDays*4+1)]
            ticks_position = [d*6*60 for d in range(nDays*4+1)]

        axs.set_xticks(ticks_position)
        axs.set_xticklabels(ticks, fontsize=fontticks)
        axs.set_xlim(xmin=0)
        axs.set_xlim(xmax=ticks_position[-1])
        axs.margins(x=0)
                                
        "primary y axis"
        if c==0:
            axs.set_yticks(np.arange(0,400.00000001,50))
            axs.set_yticklabels(np.arange(0,400.00000001,50), fontsize=fontticks) 
            axs.set_ylim(ymin=0)
            axs.set_ylim(ymax=400.00000001)        
            axs.grid(True, zorder=1, color='#EBEAEA')
            axs.margins(y=0)
            axs.set_title('Commercial activities', fontsize=fonttitles)

        if c==1:
            axs.set_yticks(np.arange(0,1600.00000001,200))
            axs.set_yticklabels(np.arange(0,1600.00000001,200), fontsize=fontticks) 
            axs.set_ylim(ymin=0)
            axs.set_ylim(ymax=1600.00000001)        
            axs.grid(True, zorder=1, color='#EBEAEA')
            axs.margins(y=0)
            axs.set_title('Domestic', fontsize=fonttitles)

        if c==2:
            axs.set_yticks(np.arange(0,80.00000001,10))
            axs.set_yticklabels(np.arange(0,80.00000001,10), fontsize=fontticks) 
            axs.set_ylim(ymin=0)
            axs.set_ylim(ymax=80.00000001)        
            axs.grid(True, zorder=1, color='#EBEAEA')
            axs.margins(y=0)
            axs.set_title('Public offices', fontsize=fonttitles)

        if c==3:
            axs.set_yticks(np.arange(0,40.00000001,5))
            axs.set_yticklabels(np.arange(0,40.00000001,5), fontsize=fontticks) 
            axs.set_ylim(ymin=0)
            axs.set_ylim(ymax=40.00000001)        
            axs.grid(True, zorder=1, color='#EBEAEA')
            axs.margins(y=0)
            axs.set_title('School', fontsize=fonttitles)

        "secondary y axis"
        ax2.set_yticks(np.arange(0,100.00000001,20))
        if c==1 or c==3:
            ax2.set_yticklabels(np.arange(0,100.00000001,20), fontsize=fontticks)
        else:
            ax2.set_yticklabels(['' for i in range(len(np.arange(0,100.00000001,20)))], fontsize=fontticks)
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=101)
        ax2.margins(y=0)
               
fig.legend(bbox_to_anchor=(0.23,0.655), ncol=1, fontsize=fontlegend, frameon=False)
fig.tight_layout()    

pylab.savefig('Figure8.pdf', format='pdf')
                    


