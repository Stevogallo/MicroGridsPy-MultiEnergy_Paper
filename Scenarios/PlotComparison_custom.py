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


configurations = ['a_Traditional-Energy-System',
                  'b_Conventional-MicroGrid',
                  'c_Multi-Good-MicroGrid',
                  'd_Multi-Energy-System']

"Import params"
StartDate = '01/07/2017 00:00:00' 
PlotScenario  = 1    
PlotStartDate = 216000    
PlotEndDate   = 216000+1441    
PlotResolution = 600   
nS = 1
nC = 4
fontticks = 14
fonttitles = 18
fontaxis = 16

idx = pd.IndexSlice

TimeSeries = {}

fig,axs = plt.subplots(2,2,figsize=(25,20))
subplot_rows = 2
subplot_cols = 2
n_row = list(itertools.chain.from_iterable(itertools.repeat(x, subplot_cols) for x in range(subplot_rows)))
n_col = list(itertools.chain.from_iterable(itertools.repeat(list(range(subplot_cols)), subplot_rows)))

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
                
        axs[n_row[k],n_col[k]].stackplot(x_Plot, y_Stacked, labels=Labels, colors=Colors)
        axs[n_row[k],n_col[k]].plot(x_Plot, y_Demand, color='black', label='Demand')
        axs[n_row[k],n_col[k]].plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_')
        
        axs[n_row[k],n_col[k]].set_ylabel('Power (kW)', fontsize=fontaxis)
    
        axs[n_row[k],n_col[k]].set_title(c, fontsize=fonttitles)

        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = ['' for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs[n_row[k],n_col[k]].set_xticks(xticks_position)
        axs[n_row[k],n_col[k]].set_xticklabels(ticks, fontsize=fontticks)    
        axs[n_row[k],n_col[k]].set_xlim(xmin=0)
        axs[n_row[k],n_col[k]].set_xlim(xmax=xticks_position[-1])
        axs[n_row[k],n_col[k]].margins(x=0)
    
        "primary y axis"
        axs[n_row[k],n_col[k]].set_yticks(np.arange(-350,351,50))
        axs[n_row[k],n_col[k]].set_yticklabels(np.arange(-350,351,50), fontsize=fontticks) 
        axs[n_row[k],n_col[k]].set_ylim(ymin=-350)
        axs[n_row[k],n_col[k]].set_ylim(ymax=351)        
        axs[n_row[k],n_col[k]].grid(True)
        
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
            
        "Plot"
        ax2=axs[n_row[k],n_col[k]].twinx()
    
        axs[n_row[k],n_col[k]].stackplot(x_Plot, y_Stacked, labels=Labels, colors=Colors)
        axs[n_row[k],n_col[k]].fill_between(x=x_Plot, y1=deltaBESS_neg, y2=0, color='#3a86ff')
        ax2.plot(x_Plot, y_BESS_SOC, '--', color='black', label='BESS state of charge')
        axs[n_row[k],n_col[k]].plot(x_Plot, y_Demand, color='black', label='_nolegend_')
        axs[n_row[k],n_col[k]].plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_')
        
        ax2.set_ylabel('State of Charge (%)', fontsize=fontaxis)
    
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = ['' for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs[n_row[k],n_col[k]].set_xticks(xticks_position)
        axs[n_row[k],n_col[k]].set_xticklabels(ticks, fontsize=fontticks)    
        axs[n_row[k],n_col[k]].set_xlim(xmin=0)
        axs[n_row[k],n_col[k]].set_xlim(xmax=xticks_position[-1])
        axs[n_row[k],n_col[k]].margins(x=0)
    
        axs[n_row[k],n_col[k]].set_title(c, fontsize=fonttitles)

        "primary y axis"
        axs[n_row[k],n_col[k]].set_yticks(np.arange(-350,351,50))
        axs[n_row[k],n_col[k]].set_yticklabels(np.arange(-350,351,50), fontsize=fontticks) 
        axs[n_row[k],n_col[k]].set_ylim(ymin=-350)
        axs[n_row[k],n_col[k]].set_ylim(ymax=351)        
        axs[n_row[k],n_col[k]].grid(True)
           
        "secondary y axis"
        ax2.set_yticks(np.arange(0,101,20))
        ax2.set_yticklabels(np.arange(0,101,20), fontsize=fontticks)
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=101)
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
            
        "Plot"
        ax2=axs[n_row[k],n_col[k]].twinx()
    
        axs[n_row[k],n_col[k]].stackplot(x_Plot, y_Stacked_pos, labels=Labels_pos, colors=Colors_pos)
        axs[n_row[k],n_col[k]].stackplot(x_Plot, y_Stacked_neg, labels=Labels_neg, colors=Colors_neg)
        ax2.plot(x_Plot, y_BESS_SOC, '--', color='black', label='_nolegend_')
        axs[n_row[k],n_col[k]].plot(x_Plot, y_Demand, color='black', label='_nolegend_')
        axs[n_row[k],n_col[k]].plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_')
 
        axs[n_row[k],n_col[k]].set_ylabel('Power (kW)', fontsize=fontaxis)
        axs[n_row[k],n_col[k]].set_xlabel('Time (Hours)', fontsize=fontaxis)

            
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = [d*6 for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs[n_row[k],n_col[k]].set_xticks(xticks_position)
        axs[n_row[k],n_col[k]].set_xticklabels(ticks, fontsize=fontticks)    
        axs[n_row[k],n_col[k]].set_xlim(xmin=0)
        axs[n_row[k],n_col[k]].set_xlim(xmax=xticks_position[-1])
        axs[n_row[k],n_col[k]].margins(x=0)
        
        axs[n_row[k],n_col[k]].set_title(c, fontsize=fonttitles)
        
        "primary y axis"
        axs[n_row[k],n_col[k]].set_yticks(np.arange(-1500,1501,250))
        axs[n_row[k],n_col[k]].set_yticklabels(np.arange(-1500,1501,250), fontsize=fontticks)  
        axs[n_row[k],n_col[k]].set_ylim(ymin=-1500)
        axs[n_row[k],n_col[k]].set_ylim(ymax=1501)        
        axs[n_row[k],n_col[k]].margins(y=0)
        axs[n_row[k],n_col[k]].grid(True)
           
        "secondary y axis"
        ax2.set_yticks(np.arange(0,101,20))
        ax2.set_yticklabels(['' for i in range(len(np.arange(0,101,20)))], fontsize=fontticks)    
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=101)
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
            
        "Plot"
        ax2=axs[n_row[k],n_col[k]].twinx()
    
        axs[n_row[k],n_col[k]].stackplot(x_Plot, y_Stacked_pos, labels=Labels_pos, colors=Colors_pos)
        axs[n_row[k],n_col[k]].stackplot(x_Plot, y_Stacked_neg, labels=Labels_neg, colors=Colors_neg)
        ax2.plot(x_Plot, y_BESS_SOC, '--', color='black', label='_nolegend_')
        axs[n_row[k],n_col[k]].plot(x_Plot, y_Demand, color='black', label='_nolegend_')
        axs[n_row[k],n_col[k]].plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_')
 
        axs[n_row[k],n_col[k]].set_xlabel('Time (Hours)', fontsize=fontaxis)
        ax2.set_ylabel('State of Charge (%)', fontsize=fontaxis)
            
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        xticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = [d*6 for d in range(nDays*4+1)]
            xticks_position = [d*6*60 for d in range(nDays*4+1)]
                
        axs[n_row[k],n_col[k]].set_xticks(xticks_position)
        axs[n_row[k],n_col[k]].set_xticklabels(ticks, fontsize=fontticks)    
        axs[n_row[k],n_col[k]].set_xlim(xmin=0)
        axs[n_row[k],n_col[k]].set_xlim(xmax=xticks_position[-1])
        axs[n_row[k],n_col[k]].margins(x=0)
        
        axs[n_row[k],n_col[k]].set_title(c, fontsize=fonttitles)
        
        "primary y axis"
        axs[n_row[k],n_col[k]].set_yticks(np.arange(-350,351,50))
        axs[n_row[k],n_col[k]].set_yticklabels(np.arange(-350,351,50), fontsize=fontticks) 
        axs[n_row[k],n_col[k]].set_ylim(ymin=-350)
        axs[n_row[k],n_col[k]].set_ylim(ymax=351)        
        axs[n_row[k],n_col[k]].margins(y=0)
        axs[n_row[k],n_col[k]].grid(True)
           
        "secondary y axis"
        ax2.set_yticks(np.arange(0,101,20))
        ax2.set_yticklabels(np.arange(0,101,20), fontsize=fontticks)
        ax2.set_ylim(ymin=0)
        ax2.set_ylim(ymax=101)
        ax2.margins(y=0)
    
        k+=1        
               
fig.legend(bbox_to_anchor=(0.18,0.97), fontsize=fontaxis, facecolor='white')
fig.tight_layout()    

pylab.savefig('ElectricDispatch_allCases.png', dpi=PlotResolution)
                    


