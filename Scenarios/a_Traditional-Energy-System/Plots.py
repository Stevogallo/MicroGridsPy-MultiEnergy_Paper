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

import warnings
warnings.filterwarnings("ignore")


#%% Electric load
def ElectricLoadCurves(resolution):

    Electric_Energy_Demand = pd.read_csv('Inputs/Electric_Demand.csv', sep=';', index_col=0) # Import electricity demand
    Electric_Energy_Demand = Electric_Energy_Demand.round(3)
    
    StartDate = '01/01/2017 00:00:00'
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
    
    plt.savefig('Results/Plots/ElectricLoadCurves.png', dpi=resolution)
    
    return

#%% Thermal loads
def ThermalLoadCurves(resolution):

    Thermal_Energy_Demand = pd.read_csv('Inputs/Thermal_Demand.csv', sep=';',  index_col=0) # Import thermal energy demand
    Thermal_Energy_Demand = Thermal_Energy_Demand.round(3)
    
    StartDate = '01/01/2017 00:00:00'
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
        
    plt.savefig('Results/Plots/ThermalLoadCurves.png', dpi=resolution)
