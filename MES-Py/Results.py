"""
Multi-Energy System (MESpy) model

Modelling framework for optimization of hybrid electric and thermal small-scale energy systems sizing

Authors: 
    Stefano Pistolese - 
    Nicolò Stevanato  - Department of Energy, Politecnico di Milano, Milan, Italy
                        Fondazione Eni Enrico Mattei, Milan, Italy
    Lorenzo Rinaldi   - Department of Energy, Politecnico di Milano, Milan, Italy
    Sergio Balderrama - Department of Mechanical and Aerospace Engineering, University of Liège, Liège, Belgium
                        San Simon University, Centro Universitario de Investigacion en Energia, Cochabamba, Bolivia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick

import warnings
warnings.filterwarnings("ignore")


#%%
def TimeSeries(instance):
    '''
    This function loads the results that depend of the periods in to a dataframe and creates a excel file with it.
    :param instance: The instance of the project resolution created by PYOMO.
    :return: A dataframe called Time_series with the values of the variables that depend of the periods.    
    '''
    
    nS = int(instance.Scenarios.extract_values()[None])
    nP = int(instance.Periods.extract_values()[None])
    nY = int(instance.Years.extract_values()[None])
    nC = int(instance.Classes.extract_values()[None])
    
    #%% Electricity Balance
    EE_Demand      = pd.DataFrame.from_dict(instance.Electric_Energy_Demand.extract_values(), orient='index')
    EE_Lost_Load   = pd.DataFrame.from_dict(instance.Lost_Load_EE.get_values(), orient='index')
    EE_RES_Prod    = pd.DataFrame.from_dict(instance.Total_RES_Energy_Production.get_values(), orient='index')
    EE_Bat_Inflow  = pd.DataFrame.from_dict(instance.Energy_Battery_Flow_In.get_values(), orient='index')
    EE_Bat_Outflow = pd.DataFrame.from_dict(instance.Energy_Battery_Flow_Out.get_values(), orient='index')
    EE_Curtailment = pd.DataFrame.from_dict(instance.Electric_Energy_Curtailment.get_values(), orient='index')
    EE_Gen_Prod    = pd.DataFrame.from_dict(instance.Total_Generator_Energy_Production.get_values(), orient='index')
    Bat_SoC        = pd.DataFrame.from_dict(instance.Battery_State_of_Charge.get_values(), orient='index')
    Diesel_Cons    = pd.DataFrame.from_dict(instance.Diesel_Consumption.get_values(), orient='index')
    
    #%%Thermal Energy Balance
    Th_Demand       = pd.DataFrame.from_dict(instance.Thermal_Energy_Demand.extract_values(), orient='index')
    Th_Lost_Load    = pd.DataFrame.from_dict(instance.Lost_Load_Th.get_values(), orient='index')
    Th_SC_Prod      = pd.DataFrame.from_dict(instance.Total_SC_Energy_Production.extract_values(), orient='index')
    Th_Tank_Outflow = pd.DataFrame.from_dict(instance.Energy_Tank_Flow_Out.extract_values(), orient='index')
    Th_Curtailment  = pd.DataFrame.from_dict(instance.Thermal_Energy_Curtailment.extract_values(), orient='index')
    Th_Boiler_Prod  = pd.DataFrame.from_dict(instance.Total_Boiler_Energy_Production.extract_values(), orient='index')
    Th_Resist_En    = pd.DataFrame.from_dict(instance.Resistance_Thermal_Energy.extract_values(), orient='index')
    Tank_SoC        = pd.DataFrame.from_dict(instance.Tank_State_of_Charge.get_values(), orient='index')
    NG_Cons         = pd.DataFrame.from_dict(instance.NG_Consumption.get_values(), orient='index')

    EE_TimeSeries = {}
    Th_TimeSeries = {}
    
    for s in range(nS):
        
       EE_TimeSeries[s] = pd.concat([EE_Demand.iloc[s*nP:(s*nP+nP),:], EE_Lost_Load.iloc[s*nP:(s*nP+nP),:], EE_RES_Prod.iloc[s*nP:(s*nP+nP),:], EE_Bat_Inflow.iloc[s*nP:(s*nP+nP),:], EE_Bat_Outflow.iloc[s*nP:(s*nP+nP),:], EE_Curtailment.iloc[s*nP:(s*nP+nP),:], EE_Gen_Prod.iloc[s*nP:(s*nP+nP),:], Bat_SoC.iloc[s*nP:(s*nP+nP),:], Diesel_Cons.iloc[s*nP:(s*nP+nP),:]], axis=1)
       EE_TimeSeries[s].columns = ['Demand','Lost Load', 'RES production', 'Bat Inflow', 'Bat Outflow', 'Curtailment', 'Genset production', 'Bat SoC', 'Diesel consumption']
       EE_TimeSeries['Sc'+str(s+1)] = EE_TimeSeries.pop(s)
       
       Th_TimeSeries[s] = {}
       
       for c in range(nC):
    
           Th_TimeSeries[s][c] = pd.concat([Th_Demand.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Lost_Load.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_SC_Prod.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Boiler_Prod.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Tank_Outflow.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Curtailment.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Resist_En.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Tank_SoC.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], NG_Cons.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:]], axis=1)
           Th_TimeSeries[s][c].columns = ['Demand','Lost Load', 'SC production', 'Boiler production', 'Tank Outflow', 'Curtailment', 'Resistance Energy', 'Tank SoC', 'NG consumption']
           Th_TimeSeries[s]['Class'+str(c+1)] = Th_TimeSeries[s].pop(c)
    
       Th_TimeSeries['Sc'+str(s+1)] = Th_TimeSeries.pop(s)
    
        
    TimeSeries = {
                  'EE': EE_TimeSeries,
                  'Th': Th_TimeSeries
                  }
    
    
    return(TimeSeries)

       
       
    
    

