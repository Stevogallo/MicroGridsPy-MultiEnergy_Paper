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

#%%
def Initialize_years(model,i):
    '''
    This function returns the value of each year of the project.     
    :param model: Pyomo model as defined in the Model_Creation script.  
    :return: The year i.
    '''    
    return i


#%% Electricity demand
Electric_Energy_Demand = pd.read_csv('Inputs/Electric_Demand.csv', index_col=0) # Import electricity demand

def Initialize_Electric_Energy_Demand(model,s,t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    :param model: Pyomo model as defined in the Model_Creation script.    
    :return: The energy demand for the period t.         
    '''
    return float(Electric_Energy_Demand.iloc[t-1,s-1])


#%% Thermal energy demand
Thermal_Energy_Demand = pd.read_csv('Inputs/Thermal_Demand.csv', index_col=0) # Import thermal energy demand

def Initialize_Thermal_Energy_Demand(model,s,c,t):
    '''
    This function returns the value of the thermal energy demand from a system for each period and classes of analysis from a excel file.
    :param model: Pyomo model as defined in the Model_Creation script.
    :return: The energy demand for the period t.     
    '''
    column=s*c
    return float(Thermal_Energy_Demand.iloc[t-1,column-1])

