# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 18:18:38 2018

@author: pisto
"""

import pandas as pd

def Initialize_years(model, i):

    '''
    This function returns the value of each year of the project. 
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The year i.
    '''    
    return i

Energy_Demand = pd.read_csv('Inputs/Electric_Demand.csv', index_col = 0) # open the electric demand demand file
Energy_Demand = Energy_Demand/1000
Energy_Demand = round(Energy_Demand, 1)

def Initialize_Demand(model, i, t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    return float(Energy_Demand.iloc[t-1,i-1])

Thermal_Energy_Demand = pd.read_csv('Inputs/Thermal_Demand.csv', index_col = 0) # open the energy thermal demand file
Thermal_Energy_Demand = Thermal_Energy_Demand/1000
Thermal_Energy_Demand = round(Thermal_Energy_Demand, 1)

def Initialize_Thermal_Demand(model, i, c, t):
    '''
    This function returns the value of the thermal energy demand from a system for each period and classes of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    column=i*c;
    
    return float(Thermal_Energy_Demand.iloc[t-1,column-1])


PV_Energy = pd.read_csv('Inputs/PV_Output.csv', index_col = 0) # open the PV energy yield file
PV_Energy = PV_Energy/1000
PV_Energy = round(PV_Energy, 1)

def Initialize_PV_Energy(model, i, t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    return float(PV_Energy.iloc[t-1,i-1])

SC_Energy = pd.read_csv('Inputs/SC_Output.csv', index_col=0) # # open the SC energy yield file
SC_Energy = SC_Energy/1000
SC_Energy = round(SC_Energy, 1)

def Initialize_SC_Energy(model, i, c, t):
    '''
    This function returns the value of the energy yield by one SC under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one SC for the class c in the period t.
    '''
    column=i*c;
    
    return float(SC_Energy.iloc[t-1,column-1])

def Marginal_Cost_Generator_1(model):
    
    return model.Diesel_Cost/(model.Low_Heating_Value*model.Generator_Effiency)

def Start_Cost(model):
    
    return model.Marginal_Cost_Generator_1*model.Generator_Nominal_Capacity*model.Cost_Increase

def Marginal_Cost_Generator(model):
    
    return (model.Marginal_Cost_Generator_1*model.Generator_Nominal_Capacity-model.Start_Cost_Generator)/model.Generator_Nominal_Capacity 

