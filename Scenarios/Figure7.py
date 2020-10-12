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
PlotStartDate = 247680    
PlotEndDate   = 247680+1441      
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

k=0
for c in configurations:
    TimeSeries[c[0]] = {}
    TimeSeries[c[0]] = {}

    TimeSeries[c[0]]['EE'] = {}
    TimeSeries[c[0]]['Th'] = {}

    for s in range(1,nS+1):
        TimeSeries[c[0]]['EE']['Sc'+str(s)] = pd.read_csv(c+'/Results/TimeSeries/Sc'+str(s)+'/EE_TimeSeries.csv', index_col=[0])


#%% Configuration A

    if c == configurations[0]:    
        "Series preparation"
        y_Genset      = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,3].values
        y_LostLoad    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,1].values
        y_Curtailment = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,2].values
        x_Plot = np.arange(len(y_Genset))
        y_Stacked = [y_Genset,
                     y_LostLoad,
                     y_Curtailment]
                        
        y_Demand   = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,0].values
        
        Colors = ['#8d99ae',
                  '#f72585',
                  '#64dfdf']
            
        Labels = ['Genset',
                  '_nolegend_',
                  '_nolegend_']        
    
        axs = plt.subplot2grid((3,2),(subplot_rows[k],subplot_cols[k]),colspan=1)

        axs.stackplot(x_Plot, y_Stacked, labels=Labels, colors=Colors, zorder=2)
        axs.plot(x_Plot, y_Demand, color='black', label='Demand', zorder=2)
        axs.plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_', zorder=2)
        
        axs.set_ylabel('Power (kW)', fontsize=fontaxis)
    
        axs.set_title('a) Traditional energy system', fontsize=fonttitles)

        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = ['' for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs.set_xticks(xticks_position)
        axs.set_xticklabels(ticks, fontsize=fontticks)    
        axs.set_xlim(xmin=0)
        axs.set_xlim(xmax=xticks_position[-1])
        axs.margins(x=0)
    
        "primary y axis"
        axs.set_yticks(np.arange(0,200.00000001,20))
        axs.set_yticklabels(np.arange(0,200.00000001,20), fontsize=fontticks) 
        axs.set_ylim(ymin=0)
        axs.set_ylim(ymax=200.00000001)        
        axs.grid(True, zorder=1, color='#EBEAEA')
        
        k+=1


#%% Configuration B        
    if c == configurations[1]:
        BESSNominalCapacity = pd.read_excel(c+'/Results/EnergySystemSize.xlsx','Size',index_col=[0,1]).loc[idx['Battery Storage System',:],'Total'].to_frame().iloc[0,0]

        "Series preparation"
        y_RES         = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,3].values
        y_BESS_out    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,4].values
        y_BESS_in     = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,5].values
        y_Genset      = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,6].values
        y_LostLoad    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,1].values
        y_Curtailment = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,2].values
        x_Plot = np.arange(len(y_Genset))
        
        deltaBESS_pos = y_BESS_out + y_BESS_in
        deltaBESS_neg = y_BESS_out + y_BESS_in
        
        for i in range(deltaBESS_pos.shape[0]):
            if deltaBESS_pos[i] < 0:   
                deltaBESS_pos[i] *= 0
            if deltaBESS_neg[i] > 0:   
                deltaBESS_neg[i] *= 0
                
        y_Stacked = [y_RES,
                     deltaBESS_pos,
                     y_Genset,
                     y_LostLoad,
                     y_Curtailment]
    
        y_Demand   = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,0].values
        y_BESS_SOC = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,-1].values/BESSNominalCapacity*100
        
        Colors = ['#ffbe0b',
                  '#3a86ff',
                  '#8d99ae',
                  '#f72585',
                  '#64dfdf']
            
        Labels = ['PV',
                  'Battery bank',
                  '_nolegend_',
                  '_nolegend_',
                  '_nolegend_']        
        
        axs = plt.subplot2grid((3,2),(subplot_rows[k],subplot_cols[k]),colspan=1)

        "Plot"
        ax2=axs.twinx()
    
        axs.stackplot(x_Plot, y_Stacked, labels=Labels, colors=Colors, zorder=2)
        axs.fill_between(x=x_Plot, y1=deltaBESS_neg, y2=0, color='#3a86ff', zorder=2)
        ax2.plot(x_Plot, y_BESS_SOC, '--', color='black', label='Battery state of charge', zorder=2)
        axs.plot(x_Plot, y_Demand, color='black', label='_nolegend_', zorder=2)
        axs.plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_', zorder=2)
        
        ax2.set_ylabel('State of Charge (%)', fontsize=fontaxis)
    
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = ['' for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs.set_xticks(xticks_position)
        axs.set_xticklabels(ticks, fontsize=fontticks)    
        axs.set_xlim(xmin=0)
        axs.set_xlim(xmax=xticks_position[-1])
        axs.margins(x=0)
    
        axs.set_title('b) Conventional micro-grid', fontsize=fonttitles)

        "primary y axis"
        axs.set_yticks(np.arange(-250,400.00000001,50))
        axs.set_yticklabels(np.arange(-250,400.00000001,50), fontsize=fontticks) 
        axs.set_ylim(ymin=-250)
        axs.set_ylim(ymax=400.00000001)        
        axs.grid(True, zorder=1, color='#EBEAEA')
           
        "secondary y axis"
        ax2.set_yticks(np.arange(0,100.00000001,20))
        ax2.set_yticklabels(np.arange(0,100.00000001,20), fontsize=fontticks)
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=100.00000001)
        ax2.margins(y=0)

        k+=1


#%% Configuration C
    if c == configurations[2]:
        BESSNominalCapacity = pd.read_excel(c+'/Results/EnergySystemSize.xlsx','Size',index_col=[0,1]).loc[idx['Battery Storage System',:],'Total'].to_frame().iloc[0,0]
    
        "Series preparation"
        y_RES         = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,4].values
        y_BESS_out    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,5].values
        y_BESS_in     = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,6].values
        y_Genset      = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,7].values
        y_ElResCons   = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,3].values
        y_LostLoad    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,1].values
        y_Curtailment = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,2].values
        x_Plot = np.arange(len(y_Genset))
        
        deltaBESS_pos = y_BESS_out + y_BESS_in
        deltaBESS_neg = y_BESS_out + y_BESS_in
        
        for i in range(deltaBESS_pos.shape[0]):
            if deltaBESS_pos[i] < 0:   
                deltaBESS_pos[i] *= 0
            if deltaBESS_neg[i] > 0:   
                deltaBESS_neg[i] *= 0
        
        y_Stacked_pos = [y_RES,
                     deltaBESS_pos,
                     y_Genset,
                     y_LostLoad,
                     y_Curtailment]
        
        y_Stacked_neg = [deltaBESS_neg,
                         y_ElResCons]
        
        y_Demand = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,0].values
        y_BESS_SOC = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,-1].values/BESSNominalCapacity*100
        
        Colors_pos = ['#ffbe0b',
                  '#3a86ff',
                  '#8d99ae',
                  '#f72585',
                  '#64dfdf']

        Colors_neg = ['#3a86ff',
                  '#aacc00']
          
        Labels_pos = ['_nolegend_',
                  '_nolegend_',
                  '_nolegend_',
                  '_nolegend_',
                  '_nolegend_']        

        Labels_neg = ['_nolegend_',
                  'Resistance']        

        axs = plt.subplot2grid((3,2),(subplot_rows[k],subplot_cols[k]),colspan=1)

        "Plot"
        ax2=axs.twinx()
    
        axs.stackplot(x_Plot, y_Stacked_pos, labels=Labels_pos, colors=Colors_pos, zorder=2)
        axs.stackplot(x_Plot, y_Stacked_neg, labels=Labels_neg, colors=Colors_neg, zorder=2)
        ax2.plot(x_Plot, y_BESS_SOC, '--', color='black', label='_nolegend_', zorder=2)
        axs.plot(x_Plot, y_Demand, color='black', label='_nolegend_', zorder=2)
        axs.plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_', zorder=2)
 
        axs.set_ylabel('Power (kW)', fontsize=fontaxis)
        axs.set_xlabel('Time (Hours)', fontsize=fontaxis)

            
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = [d*6 for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs.set_xticks(xticks_position)
        axs.set_xticklabels(ticks, fontsize=fontticks)    
        axs.set_xlim(xmin=0)
        axs.set_xlim(xmax=xticks_position[-1])
        axs.margins(x=0)
        
        axs.set_title('c) Multi-good micro-grid', fontsize=fonttitles)
        
        "primary y axis"
        axs.set_yticks(np.arange(-1500,1500.00000001,250))
        axs.set_yticklabels(np.arange(-1500,1500.00000001,250), fontsize=fontticks)  
        axs.set_ylim(ymin=-1500)
        axs.set_ylim(ymax=1500.00000001)        
        axs.margins(y=0)
        axs.grid(True, zorder=1, color='#EBEAEA')
           
        "secondary y axis"
        ax2.set_yticks(np.arange(0,100.00000001,20))
        ax2.set_yticklabels(['' for i in range(len(np.arange(0,101,20)))], fontsize=fontticks)    
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=100.00000001)
        ax2.margins(y=0)
    
        k+=1


#%% Configuration D
    if c == configurations[3]:
        BESSNominalCapacity = pd.read_excel(c+'/Results/EnergySystemSize.xlsx','Size',index_col=[0,1]).loc[idx['Battery Storage System',:],'Total'].to_frame().iloc[0,0]
    
        "Series preparation"
        y_RES         = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,4].values
        y_BESS_out    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,5].values
        y_BESS_in     = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,6].values
        y_Genset      = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,7].values
        y_ElResCons   = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,3].values
        y_LostLoad    = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,1].values
        y_Curtailment = -1*TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,2].values
        x_Plot = np.arange(len(y_Genset))
        
        deltaBESS_pos = y_BESS_out + y_BESS_in
        deltaBESS_neg = y_BESS_out + y_BESS_in
        
        for i in range(deltaBESS_pos.shape[0]):
            if deltaBESS_pos[i] < 0:   
                deltaBESS_pos[i] *= 0
            if deltaBESS_neg[i] > 0:   
                deltaBESS_neg[i] *= 0
        
        y_Stacked_pos = [y_RES,
                     deltaBESS_pos,
                     y_Genset,
                     y_LostLoad,
                     y_Curtailment]
        
        y_Stacked_neg = [deltaBESS_neg,
                         y_ElResCons]
        
        y_Demand = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,0].values
        y_BESS_SOC = TimeSeries[c[0]]['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,-1].values/BESSNominalCapacity*100
        
        Colors_pos = ['#ffbe0b',
                  '#3a86ff',
                  '#8d99ae',
                  '#f72585',
                  '#64dfdf']

        Colors_neg = ['#3a86ff',
                  '#aacc00']
          
        Labels_pos = ['_nolegend_',
                  '_nolegend_',
                  '_nolegend_',
                  'Lost load',
                  'Curtailment']        

        Labels_neg = ['_nolegend_',
                  '_nolegend_']        

        axs = plt.subplot2grid((3,2),(subplot_rows[k],subplot_cols[k]),colspan=1)

        "Plot"
        ax2=axs.twinx()
    
        axs.stackplot(x_Plot, y_Stacked_pos, labels=Labels_pos, colors=Colors_pos, zorder=2)
        axs.stackplot(x_Plot, y_Stacked_neg, labels=Labels_neg, colors=Colors_neg, zorder=2)
        ax2.plot(x_Plot, y_BESS_SOC, '--', color='black', label='_nolegend_', zorder=2)
        axs.plot(x_Plot, y_Demand, color='black', label='_nolegend_', zorder=2)
        axs.plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_', zorder=2)
 
        axs.set_xlabel('Time (Hours)', fontsize=fontaxis)
        ax2.set_ylabel('State of Charge (%)', fontsize=fontaxis)
            
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = [d*6 for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs.set_xticks(xticks_position)
        axs.set_xticklabels(ticks, fontsize=fontticks)    
        axs.set_xlim(xmin=0)
        axs.set_xlim(xmax=xticks_position[-1])
        axs.margins(x=0)
        
        axs.set_title('d) Integrated multi-energy system', fontsize=fonttitles)
        
        "primary y axis"
        axs.set_yticks(np.arange(-300,400.00000001,50))
        axs.set_yticklabels(np.arange(-300,400.00000001,50), fontsize=fontticks) 
        axs.set_ylim(ymin=-300)
        axs.set_ylim(ymax=400.00000001)        
        axs.margins(y=0)
        axs.grid(True, zorder=1, color='#EBEAEA')
           
        "secondary y axis"
        ax2.set_yticks(np.arange(0,100.00000001,20))
        ax2.set_yticklabels(np.arange(0,100.00000001,20), fontsize=fontticks)
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=100.00000001)
        ax2.margins(y=0)
    
        k+=1        
               
fig.legend(bbox_to_anchor=(0.455,0.655), ncol=2, fontsize=fontlegend, frameon=False)
fig.tight_layout()    

pylab.savefig('Figure7_21Jun.svg', format='svg')
                    


