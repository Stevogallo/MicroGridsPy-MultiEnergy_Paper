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


#%% Electric load
def ElectricLoadCurves(StartDate,PlotResolution):

    Electric_Energy_Demand = pd.read_csv('Inputs/Electric_Demand.csv', sep=';', index_col=0) # Import electricity demand
    Electric_Energy_Demand = Electric_Energy_Demand.round(3)
    
    Electric_Energy_Demand.index = pd.DatetimeIndex(start=StartDate, periods=525600, freq='1min')
    
    StartDatePlot = ['12/21/2017 00:00:00','03/21/2017 00:00:00','06/21/2017 00:00:00','09/23/2017 00:00:00'] # MM/DD/YY
    EndDatePlot   = ['12/21/2017 23:59:59','03/21/2017 23:59:59','06/21/2017 23:59:59','09/23/2017 23:59:59']
    
    y_Plot1 = Electric_Energy_Demand.loc[StartDatePlot[0]:EndDatePlot[0], :].values
    y_Plot2 = Electric_Energy_Demand.loc[StartDatePlot[1]:EndDatePlot[1], :].values
    y_Plot3 = Electric_Energy_Demand.loc[StartDatePlot[2]:EndDatePlot[2], :].values
    y_Plot4 = Electric_Energy_Demand.loc[StartDatePlot[3]:EndDatePlot[3], :].values
    x_Plot  = np.arange(len(y_Plot1))
    
    plt.figure(figsize=(15,6))
    
    plt.plot(x_Plot, y_Plot4, '#2e279d', label='Spring')
    plt.plot(x_Plot, y_Plot1, '#4d80e4', label='Summer')
    plt.plot(x_Plot, y_Plot2, '#46b3e6', label='Fall')
    plt.plot(x_Plot, y_Plot3, '#dff6f0', label='Winter')
    
    plt.ylabel('Power (kW)', fontsize=14)
    plt.xlabel('Time (Hours)', fontsize=14)
    
    plt.ylim(ymin=0)
    plt.ylim(ymax=200)
    
    plt.margins(x=0)
    plt.margins(y=0)
    
    plt.xticks([0,(4*60),(8*60),(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])#, fontsize=14)
    # plt.yticks(fontsize=14)
    
    plt.grid(True)
    plt.legend(loc='upper left', fontsize='15', facecolor='white')
    
    plt.savefig('Results/Plots/ElectricLoadCurves.png', dpi=PlotResolution)
    
    return


#%% Thermal loads
def ThermalLoadCurves(StartDate,PlotResolution):

    Thermal_Energy_Demand = pd.read_csv('Inputs/Thermal_Demand.csv', sep=';',  index_col=0) # Import thermal energy demand
    Thermal_Energy_Demand = Thermal_Energy_Demand.round(3)
    
    Thermal_Energy_Demand.index = pd.DatetimeIndex(start=StartDate, periods=525600, freq='1min')
    
    StartDatePlot = ['12/23/2017 00:00:00','03/23/2017 00:00:00','06/23/2017 00:00:00','09/23/2017 00:00:00'] # MM/DD/YY
    EndDatePlot   = ['12/23/2017 23:59:59','03/23/2017 23:59:59','06/23/2017 23:59:59','09/23/2017 23:59:59']
    
    fig, axs = plt.subplots(2,2, figsize=(15,12))
    
    subplot_rows = [0,0,1,1]
    subplot_cols = [0,1,0,1]
    
    ymax = [350,1200,100,100]
    
    i = 0
    for c in Thermal_Energy_Demand.columns:
        y_Plot1 = Thermal_Energy_Demand.loc[StartDatePlot[0]:EndDatePlot[0], c].values
        y_Plot2 = Thermal_Energy_Demand.loc[StartDatePlot[1]:EndDatePlot[1], c].values
        y_Plot3 = Thermal_Energy_Demand.loc[StartDatePlot[2]:EndDatePlot[2], c].values
        y_Plot4 = Thermal_Energy_Demand.loc[StartDatePlot[3]:EndDatePlot[3], c].values
        x_Plot  = np.arange(len(y_Plot1))
        
        axs[subplot_rows[i],subplot_cols[i]].plot(x_Plot, y_Plot4, '#8fcfd1', label='Spring')
        axs[subplot_rows[i],subplot_cols[i]].plot(x_Plot, y_Plot1, '#df5e88', label='Summer')
        axs[subplot_rows[i],subplot_cols[i]].plot(x_Plot, y_Plot2, '#f6ab6c', label='Fall')
        axs[subplot_rows[i],subplot_cols[i]].plot(x_Plot, y_Plot3, '#f6efa6', label='Winter')
    
        axs[0,0].set_ylabel('Power (kW)', fontsize=14)
        axs[1,0].set_ylabel('Power (kW)', fontsize=14)
        axs[1,0].set_xlabel('Time (Hours)', fontsize=14)
        axs[1,1].set_xlabel('Time (Hours)', fontsize=14)
        
        axs[subplot_rows[i],subplot_cols[i]].set_ylim(ymin=0)
        axs[subplot_rows[i],subplot_cols[i]].set_ylim(ymax=ymax[i])
    
        axs[subplot_rows[i],subplot_cols[i]].margins(x=0)
        axs[subplot_rows[i],subplot_cols[i]].margins(y=0)
                
        axs[subplot_rows[i],subplot_cols[i]].set_xticks([0,(4*60),(8*60),(60*12),(60*16),(60*20),(60*24)])
        axs[subplot_rows[i],subplot_cols[i]].set_xticklabels([0,4,8,12,16,20,24])#, fontsize=14)
    
        # axs[0,0].set_yticklabels(np.arange(0,ymax[i],ymax[i]/6), fontsize=14)
        # axs[0,1].set_yticklabels(np.arange(0,ymax[i],ymax[i]/6), fontsize=14)
        # axs[1,0].set_yticklabels(np.arange(0,ymax[i],ymax[i]/6), fontsize=14)
        # axs[1,1].set_yticklabels(np.arange(0,ymax[i],ymax[i]/6), fontsize=14)
        
        axs[0,0].set_title('Commercial loads', fontsize=14)
        axs[0,1].set_title('Domestic loads', fontsize=14)
        axs[1,0].set_title('Public loads', fontsize=14)
        axs[1,1].set_title('School loads', fontsize=14)
    
        axs[subplot_rows[i],subplot_cols[i]].grid(True)
        
        axs[0,0].legend(loc='upper left', fontsize='15', facecolor='white')
    
        i += 1
        
    plt.savefig('Results/Plots/ThermalLoadCurves.png', dpi=PlotResolution)

    return


#%% Electric dispatch
def ElectricDispatch(nS,PlotScenario,PlotStartDate,PlotEndDate,PlotResolution):

    "Import"
    TimeSeries = {}
    TimeSeries['EE'] = {}
    for s in range(1,nS+1):
        TimeSeries['EE']['Sc'+str(s)] = pd.read_csv('Results/TimeSeries/Sc'+str(s)+'/EE_TimeSeries.csv', index_col=[0])
    
    idx = pd.IndexSlice
    
    "Series preparation"
    y_Genset      = TimeSeries['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,3].values
    y_LostLoad    = TimeSeries['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,1].values
    y_Curtailment = -1*TimeSeries['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,2].values
    x_Plot = np.arange(len(y_Genset))
    y_Stacked = [y_Genset,
                 y_LostLoad,
                 y_Curtailment]
                    
    y_Demand   = TimeSeries['EE']['Sc'+str(PlotScenario)].iloc[PlotStartDate:PlotEndDate,0].values
    
    Colors = ['#8d99ae',
              '#f72585',
              '#64dfdf']
        
    Labels = ['Genset',
              'Lost Load',
              'Curtailment']        
        
    "Plot"
    fig,ax = plt.subplots(figsize=(20,10))

    ax.stackplot(x_Plot, y_Stacked, labels=Labels, colors=Colors)
    ax.plot(x_Plot, y_Demand, color='black', label='Demand')
    ax.plot(x_Plot, np.zeros((len(x_Plot))), color='black', label='_nolegend_')
    
    ax.set_ylabel('Power (kW)', fontsize=14)
    ax.set_xlabel('Time (Hours)', fontsize=14)

    "x axis"
    nDays = int(len(x_Plot)/1440)    
    xticks_position = []
    ticks = []
    for i in range(1,nDays+1):
        ticks = [d*6 for d in range(nDays*4+1)]
        xticks_position = [d*6*60 for d in range(nDays*4+1)]
            
    ax.set_xticks(xticks_position)
    ax.set_xticklabels(ticks, fontsize=14)    
    ax.set_xlim(xmin=0)
    ax.set_xlim(xmax=xticks_position[-1])
    ax.margins(x=0)

    "primary y axis"
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14) 
    ax.margins(y=0)
    ax.grid(True)
           
    fig.legend(bbox_to_anchor=(0.21,0.82), fontsize=14, facecolor='white')
    
    pylab.savefig('Results/Plots/ElectricDispatch.png', bbox_inches='tight', dpi=PlotResolution)
                    
    return


#%% ThermalDispatch
def ThermalDispatch(nC,nS,PlotScenario,PlotStartDate,PlotEndDate,PlotResolution):
    
    "Import"
    TimeSeries = {}
    TimeSeries['Th'] = {}
    for s in range(1,nS+1):
        TimeSeries['Th']['Sc'+str(s)] = {}
        for c in range(1,nC+1):
            TimeSeries['Th']['Sc'+str(s)]['Class'+str(c)] = pd.read_csv('Results/TimeSeries/Sc'+str(s)+'/Th_TimeSeries_Class'+str(c)+'.csv', index_col=[0])
    
    fig,axs = plt.subplots(2,2,figsize=(20,20))
    subplot_rows = 2
    subplot_cols = 2
    n_row = list(itertools.chain.from_iterable(itertools.repeat(x, subplot_cols) for x in range(subplot_rows)))
    n_col = list(itertools.chain.from_iterable(itertools.repeat(list(range(subplot_cols)), subplot_rows)))
    idx = pd.IndexSlice

    for c in range(1,nC+1):
        "Series preparation"
        y_Boiler      = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c)].iloc[PlotStartDate:PlotEndDate,2].values
        y_LostLoad    = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c)].iloc[PlotStartDate:PlotEndDate,1].values
        y_Curtailment = -1*TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c)].iloc[PlotStartDate:PlotEndDate,3].values
        x_Plot = np.arange(len(y_Boiler))
        y_Stacked = [y_Boiler,
                     y_LostLoad,
                     y_Curtailment]
    
        y_Demand = TimeSeries['Th']['Sc'+str(PlotScenario)]['Class'+str(c)].iloc[PlotStartDate:PlotEndDate,0].values
    
        Colors = ['#8d99ae',
                  '#f72585',
                  '#64dfdf']
        if c==1: 
            Labels = ['Boiler',
                      'Lost Load',
                      'Curtailment']        
        else:
            Labels = ['_nolegend_','_nolegend_','_nolegend_']
       
        "Plot"
        axs[n_row[c-1],n_col[c-1]].stackplot(x_Plot, y_Stacked, labels=Labels, colors=Colors)
        if c==1:
            axs[n_row[c-1],n_col[c-1]].plot(x_Plot, y_Demand, color='black', label='Demand')
        else:
            axs[n_row[c-1],n_col[c-1]].plot(x_Plot, y_Demand, color='black', label='_nolegend_')

        if c==1 or c==3:
            axs[n_row[c-1],n_col[c-1]].set_ylabel('Power (kW)', fontsize=14)
        if c==3 or c==4:
            axs[n_row[c-1],n_col[c-1]].set_xlabel('Time (Hours)', fontsize=14)
    
        "x axis"
        nDays = int(len(x_Plot)/1440)    
        ticks_position = []
        ticks = []
        for i in range(1,nDays+1):
            ticks = [d*6 for d in range(nDays*4+1)]
            ticks_position = [d*6*60 for d in range(nDays*4+1)]

        axs[n_row[c-1],n_col[c-1]].set_xticks(ticks_position)
        axs[n_row[c-1],n_col[c-1]].set_xticklabels(ticks, fontsize=14)
        axs[n_row[c-1],n_col[c-1]].set_xlim(xmin=0)
        axs[n_row[c-1],n_col[c-1]].set_xlim(xmax=ticks_position[-1])
        axs[n_row[c-1],n_col[c-1]].margins(x=0)
                                
        "primary y axis"
        for tick in axs[n_row[c-1],n_col[c-1]].yaxis.get_major_ticks():
                tick.label.set_fontsize(14) 
        axs[n_row[c-1],n_col[c-1]].margins(y=0)
        axs[n_row[c-1],n_col[c-1]].grid(True)   
        
            
    fig.legend(bbox_to_anchor=(0.185,0.985), fontsize=14, facecolor='white')
            
    plt.tight_layout()
    pylab.savefig('Results/Plots/ThermalDispatch.png', bbox_inches='tight', dpi=PlotResolution)

    return





