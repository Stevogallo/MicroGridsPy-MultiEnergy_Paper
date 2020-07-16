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
import numpy as np
import os
from pandas import ExcelWriter

import warnings
warnings.filterwarnings("ignore")


#%% Energy balances
def TimeSeries(instance):
    
    nS = int(instance.Scenarios.extract_values()[None])
    nP = int(instance.Periods.extract_values()[None])
    nY = int(instance.Years.extract_values()[None])
    nC = int(instance.Classes.extract_values()[None])

    StartDate = instance.StartDate.extract_values()[None]
    dateInd = pd.DatetimeIndex(start=StartDate, periods=nP, freq='1min')

    
    #%% Electricity balance terms
    EE_Demand      = pd.DataFrame.from_dict(instance.Electric_Energy_Demand.extract_values(), orient='index')
    EE_Lost_Load   = pd.DataFrame.from_dict(instance.Lost_Load_EE.get_values(), orient='index')
    EE_Curtailment = pd.DataFrame.from_dict(instance.Electric_Energy_Curtailment.get_values(), orient='index')
    EE_Gen_Prod    = pd.DataFrame.from_dict(instance.Total_Generator_Energy_Production.get_values(), orient='index')
    # Additional useful terms
    Diesel_Cons    = pd.DataFrame.from_dict(instance.Diesel_Consumption.get_values(), orient='index')
    
    
    #%%Thermal energy balance terms
    Th_Demand       = pd.DataFrame.from_dict(instance.Thermal_Energy_Demand.extract_values(), orient='index')
    Th_Lost_Load    = pd.DataFrame.from_dict(instance.Lost_Load_Th.get_values(), orient='index')
    Th_Curtailment  = pd.DataFrame.from_dict(instance.Thermal_Energy_Curtailment.extract_values(), orient='index')
    Th_Boiler_Prod  = pd.DataFrame.from_dict(instance.Total_Boiler_Energy_Production.extract_values(), orient='index')
    # Additional useful terms
    NG_Cons         = pd.DataFrame.from_dict(instance.NG_Consumption.get_values(), orient='index')


    #%% Preparing for export
    EE_TimeSeries = {}
    Th_TimeSeries = {}
    
    for s in range(nS):
        
       EE_TimeSeries[s] = pd.concat([EE_Demand.iloc[s*nP:(s*nP+nP),:], EE_Lost_Load.iloc[s*nP:(s*nP+nP),:], EE_Curtailment.iloc[s*nP:(s*nP+nP),:], EE_Gen_Prod.iloc[s*nP:(s*nP+nP),:], Diesel_Cons.iloc[s*nP:(s*nP+nP),:]], axis=1)
       EE_TimeSeries[s].columns = ['Demand','Lost Load', 'Curtailment', 'Genset production', 'Diesel consumption']
       EE_TimeSeries[s].index = dateInd
       EE_TimeSeries['Sc'+str(s+1)] = EE_TimeSeries.pop(s)
       EE_path = 'Results/TimeSeries/Sc'+str(s+1)
       if not os.path.exists(EE_path):
           os.makedirs(EE_path)
       EE_TimeSeries['Sc'+str(s+1)].to_csv(EE_path+'/EE_TimeSeries.csv')
       
       Th_TimeSeries[s] = {}
       
       for c in range(nC):
    
           Th_TimeSeries[s][c] = pd.concat([Th_Demand.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Lost_Load.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Boiler_Prod.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Curtailment.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], NG_Cons.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:]], axis=1)
           Th_TimeSeries[s][c].columns = ['Demand','Lost Load', 'Boiler production', 'Curtailment', 'NG consumption']
           Th_TimeSeries[s][c].index = dateInd
           Th_TimeSeries[s]['Class'+str(c+1)] = Th_TimeSeries[s].pop(c)
           
       Th_TimeSeries['Sc'+str(s+1)] = Th_TimeSeries.pop(s)
   
       for c in range(nC):
           Th_path = 'Results/TimeSeries/Sc'+str(s+1)
           if not os.path.exists(EE_path):
               os.makedirs(EE_path)
           Th_TimeSeries['Sc'+str(s+1)]['Class'+str(c+1)].to_csv(Th_path+'/Th_TimeSeries_Class'+str(c+1)+'.csv')
                                                                  
    TimeSeries = {'EE': EE_TimeSeries,
                  'Th': Th_TimeSeries}
    
    return(TimeSeries)


#%% Energy System Configuration
def EnergySystemInfo(instance):
    
    #%% System size
    nS = int(instance.Scenarios.extract_values()[None])
    nP = int(instance.Periods.extract_values()[None])
    nY = int(instance.Years.extract_values()[None])
    nC = int(instance.Classes.extract_values()[None])
    dr = instance.Discount_Rate.extract_values()[None]

    # Electricity system components
          
    Gen_Capacity = pd.DataFrame(['Genset', 'kW', instance.Generator_Nominal_Capacity.get_values()[None]/1000]).T.set_index([0,1])
    
    EE_system = pd.concat([Gen_Capacity], axis=0)
    EE_system.index.names = ['EE components', 'Unit']
    EE_system.columns = ['Total']

    
    # Thermal system components
    Boiler_Capacity = list(instance.Boiler_Nominal_Capacity.get_values().values())
    Boiler_Capacity = [i/1000 for i in Boiler_Capacity]
    Boiler_Capacity = pd.DataFrame([['NG Boiler', 'kW'] + Boiler_Capacity]).set_index([0,1])
    
            
    Th_system = pd.concat([Boiler_Capacity], axis=0)
    Th_system = pd.concat([Th_system, Th_system.sum(1).to_frame()],axis=1)
    Th_system.index.names = ['Th Components', 'Unit']
    Th_system.columns = ['Class'+str(c+1) for c in range(nC)]+['Total']
    
    EnergySystemSize = pd.concat([EE_system, Th_system],axis=0).fillna("-")
    


    #%% Economic analysis
    NPC = pd.DataFrame(['Net Present Cost', 'MUSD', instance.ObjectiveFuntion.expr()/1e6]).T.set_index([0,1])
    NPC.columns = ['Total']
    
    #%% Investment cost   
    Gen_Capacity = instance.Generator_Nominal_Capacity.get_values()[None]
    Gen_Specific_Investment_Cost = instance.Generator_Invesment_Cost.extract_values()[None]
    Gen_Investment_Cost = pd.DataFrame(['Investment Cost', 'Genset', 'MUSD', Gen_Capacity*Gen_Specific_Investment_Cost/1e6]).T.set_index([0,1,2])
    Gen_Investment_Cost.columns = ['Total']
    
    Boiler_Specific_Investment_Cost = instance.Boiler_Invesment_Cost.extract_values()[None]
    Boiler_Capacity = list(instance.Boiler_Nominal_Capacity.get_values().values())
    Boiler_Investment_Cost = pd.DataFrame(np.multiply(Boiler_Capacity, Boiler_Specific_Investment_Cost/1e6)).T 
    Boiler_Investment_Cost = pd.concat([pd.DataFrame(['Investment Cost', 'NG Boiler', 'MUSD']).T,Boiler_Investment_Cost], axis=1)
    Boiler_Investment_Cost.columns = np.arange(Boiler_Investment_Cost.shape[1])
    Boiler_Investment_Cost = Boiler_Investment_Cost.set_index([0,1,2])

    #%% O&M cost   
    Gen_OM_Cost = pd.DataFrame()
    Boiler_OM_Cost = pd.DataFrame()
    
    for y in range(1,nY+1):
        Gen_OM_Cost = pd.concat([Gen_OM_Cost, pd.DataFrame(['O&M Cost', str(y),'Genset', 'MUSD', instance.Generator_Nominal_Capacity.extract_values()[None]*instance.Generator_Invesment_Cost.extract_values()[None]*instance.Generator_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y]).T.set_index([0,1,2,3])],axis=0)
        
        Boiler_OM_Cost = pd.concat([Boiler_OM_Cost, pd.concat([pd.DataFrame(['O&M Cost', str(y),'NG Boiler', 'MUSD']).T, pd.DataFrame([i*instance.Boiler_Invesment_Cost.extract_values()[None]*instance.Boiler_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y for i in instance.Boiler_Nominal_Capacity.extract_values()]).T],axis=1)],axis=0)
        
    Gen_OM_Cost.columns = ['Total']
        
    Boiler_OM_Cost.columns = np.arange(Boiler_OM_Cost.shape[1])        
    Boiler_OM_Cost = Boiler_OM_Cost.set_index([0,1,2,3])
    Boiler_OM_Cost.columns = ['Class'+str(c+1) for c in range(nC)]
       

    #%% Concatenating
    EE_Inv_Cost = pd.concat([Gen_Investment_Cost], axis=0)
    EE_Inv_Cost.index.names = ['Cost item', 'Component', 'Unit']
    
    Th_Inv_Cost = pd.concat([Boiler_Investment_Cost], axis=0)
    Th_Inv_Cost.index.names = ['Cost item', 'Component', 'Unit']
    Th_Inv_Cost = pd.concat([Th_Inv_Cost, Th_Inv_Cost.sum(1).to_frame()],axis=1)      
    Th_Inv_Cost.columns = ['Class'+str(c+1) for c in range(nC)]+['Total']

    EE_OM_Cost = pd.concat([Gen_OM_Cost], axis=0).groupby(level=[0,2,3],axis=0,sort=False).sum()
    EE_OM_Cost.index.names = ['Cost item', 'Component', 'Unit']
    
    Th_tot_OM_Cost = pd.concat([Boiler_OM_Cost], axis=0).groupby(level=[0,2,3],axis=0,sort=False).sum()
    Th_tot_OM_Cost.index.names = ['Cost item', 'Component', 'Unit']
    Th_tot_OM_Cost = pd.concat([Th_tot_OM_Cost, Th_tot_OM_Cost.sum(1).to_frame()],axis=1)      
    Th_tot_OM_Cost.columns = ['Class'+str(c+1) for c in range(nC)]+['Total']


    EnergySystemCost = pd.concat([EE_Inv_Cost, Th_Inv_Cost, EE_OM_Cost, Th_tot_OM_Cost],axis=0).fillna("-")
    
    
    #%% Export
    ESs_path = 'Results'
    if not os.path.exists(ESs_path):
        os.makedirs(ESs_path)
    
    ESsFile = ExcelWriter(ESs_path+'/EnergySystemSize.xlsx')
    EnergySystemSize.to_excel(ESsFile, sheet_name='Size')   
    EnergySystemCost.to_excel(ESsFile, sheet_name='Cost')   
    
    ESsFile.save()
           
    
    return(EnergySystemSize, EnergySystemCost)

    

