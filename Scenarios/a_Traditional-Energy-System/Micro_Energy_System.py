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

import time
start = time.time()

plotMode = 'Off'


if plotMode != 'On':
    
    from pyomo.environ import AbstractModel
    from Results import TimeSeries, EnergySystemInfo
    from Model_Creation import Model_Creation
    from Model_Resolution import Model_Resolution
    from Plots import ElectricLoadCurves,ThermalLoadCurves,ElectricDispatch,ThermalDispatch

    model = AbstractModel()  # Define type of optimization problem

    #%% Optimization model
    Model_Creation(model)  # Creation of the Sets, parameters and variables.
    instance = Model_Resolution(model)  # Resolution of the instance
    
    #%% Result export
    TimeSeries = TimeSeries(instance)  # Extract the results of energy from the instance and save it in a excel file 
    EnergySystemSize,EnergySystemCost,EnergyIndicators = EnergySystemInfo(instance)
    
    #%% Plot
    ElectricLoadCurves(instance)
    ThermalLoadCurves(instance)
    ElectricDispatch(instance,TimeSeries)
    ThermalDispatch(instance,TimeSeries)

else:
    import pandas as pd
    from PlotMode import ElectricLoadCurves,ThermalLoadCurves,ElectricDispatch,ThermalDispatch
    
    idx = pd.IndexSlice
    
    "Import params"
    StartDate = '01/07/2017 00:00:00' 
    PlotScenario  = 1    
    PlotStartDate = 216000    
    PlotEndDate   = 216000+1441    
    PlotResolution = 300   
    nS = 1
    nC = 4

    ElectricLoadCurves(StartDate,PlotResolution)
    ThermalLoadCurves(StartDate,PlotResolution)
    ElectricDispatch(nS,PlotScenario,PlotStartDate,PlotEndDate,PlotResolution)
    ThermalDispatch(nC,nS,PlotScenario,PlotStartDate,PlotEndDate,PlotResolution)
    

end = time.time()
elapsed = end - start
print("\nTime: ",round(elapsed/60,0),"min")

