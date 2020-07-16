"""
Multi-Energy System (MESpy) model

Modelling framework for optimization of hybrid electric and thermal small-scale energy systems sizing

Authors: 
    Stefano Pistolese - Department of Energy, Politecnico di Milano, Milan, Italy
    Nicolò Stevanato  - Department of Energy, Politecnico di Milano, Milan, Italy
                        Fondazione Eni Enrico Mattei, Milan, Italy
    Lorenzo Rinaldi   - Department of Energy, Politecnico di Milano, Milan, Italy
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
# Electric_Energy_Demand = Electric_Energy_Demand/1000      # Convert in kW
# Electric_Energy_Demand = round(Electric_Energy_Demand, 1) 

def Initialize_Electric_Energy_Demand(model,i,t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    :param model: Pyomo model as defined in the Model_Creation script.    
    :return: The energy demand for the period t.         
    '''
    return float(Electric_Energy_Demand.iloc[t-1,i-1])


#%% Thermal energy demand
Thermal_Energy_Demand = pd.read_csv('Inputs/Thermal_Demand.csv', index_col=0) # Import thermal energy demand
# Thermal_Energy_Demand = Thermal_Energy_Demand/1000
# Thermal_Energy_Demand = round(Thermal_Energy_Demand, 1)

def Initialize_Thermal_Energy_Demand(model,i,c,t):
    '''
    This function returns the value of the thermal energy demand from a system for each period and classes of analysis from a excel file.
    :param model: Pyomo model as defined in the Model_Creation script.
    :return: The energy demand for the period t.     
    '''
    column=i*c
    return float(Thermal_Energy_Demand.iloc[t-1,column-1])


#%% PV output
RES_Energy_Output = pd.read_csv('Inputs/RES_Energy_Output.csv', index_col=0)  # Import PV energy generation profile
# RES_Energy_Output = RES_Energy_Output/1000
# RES_Energy_Output = round(RES_Energy_Output, 1)

def Initialize_RES_Energy(model, i, t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    :param model: Pyomo model as defined in the Model_Creation script.
    :return: The energy yield of one PV for the period t.
    '''
    return float(RES_Energy_Output.iloc[t-1,i-1])

