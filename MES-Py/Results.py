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
    EE_RES_Prod    = pd.DataFrame.from_dict(instance.Total_RES_Energy_Production.get_values(), orient='index')
    EE_Bat_Inflow  = pd.DataFrame.from_dict(instance.Energy_Battery_Flow_In.get_values(), orient='index')
    EE_Bat_Outflow = pd.DataFrame.from_dict(instance.Energy_Battery_Flow_Out.get_values(), orient='index')
    EE_Curtailment = pd.DataFrame.from_dict(instance.Electric_Energy_Curtailment.get_values(), orient='index')
    EE_Gen_Prod    = pd.DataFrame.from_dict(instance.Total_Generator_Energy_Production.get_values(), orient='index')
    # Additional useful terms
    Bat_SoC        = pd.DataFrame.from_dict(instance.Battery_State_of_Charge.get_values(), orient='index')
    Diesel_Cons    = pd.DataFrame.from_dict(instance.Diesel_Consumption.get_values(), orient='index')
    
    
    #%%Thermal energy balance terms
    Th_Demand       = pd.DataFrame.from_dict(instance.Thermal_Energy_Demand.extract_values(), orient='index')
    Th_Lost_Load    = pd.DataFrame.from_dict(instance.Lost_Load_Th.get_values(), orient='index')
    Th_SC_Prod      = pd.DataFrame.from_dict(instance.Total_SC_Energy_Production.extract_values(), orient='index')
    Th_Tank_Outflow = pd.DataFrame.from_dict(instance.Energy_Tank_Flow_Out.extract_values(), orient='index')
    Th_Curtailment  = pd.DataFrame.from_dict(instance.Thermal_Energy_Curtailment.extract_values(), orient='index')
    Th_Boiler_Prod  = pd.DataFrame.from_dict(instance.Total_Boiler_Energy_Production.extract_values(), orient='index')
    Th_Resist_En    = pd.DataFrame.from_dict(instance.Resistance_Thermal_Energy.extract_values(), orient='index')
    # Additional useful terms
    Tank_SoC        = pd.DataFrame.from_dict(instance.Tank_State_of_Charge.get_values(), orient='index')
    NG_Cons         = pd.DataFrame.from_dict(instance.NG_Consumption.get_values(), orient='index')


    #%% Preparing for export
    EE_TimeSeries = {}
    Th_TimeSeries = {}
    
    for s in range(nS):
        
       EE_TimeSeries[s] = pd.concat([EE_Demand.iloc[s*nP:(s*nP+nP),:], EE_Lost_Load.iloc[s*nP:(s*nP+nP),:], EE_RES_Prod.iloc[s*nP:(s*nP+nP),:], EE_Bat_Inflow.iloc[s*nP:(s*nP+nP),:], EE_Bat_Outflow.iloc[s*nP:(s*nP+nP),:], EE_Curtailment.iloc[s*nP:(s*nP+nP),:], EE_Gen_Prod.iloc[s*nP:(s*nP+nP),:], Bat_SoC.iloc[s*nP:(s*nP+nP),:], Diesel_Cons.iloc[s*nP:(s*nP+nP),:]], axis=1)
       EE_TimeSeries[s].columns = ['Demand','Lost Load', 'RES production', 'Bat Inflow', 'Bat Outflow', 'Curtailment', 'Genset production', 'Bat SoC', 'Diesel consumption']
       EE_TimeSeries[s].index = dateInd
       EE_TimeSeries['Sc'+str(s+1)] = EE_TimeSeries.pop(s)
       EE_path = 'Results/TimeSeries/Sc'+str(s+1)
       if not os.path.exists(EE_path):
           os.makedirs(EE_path)
       EE_TimeSeries['Sc'+str(s+1)].to_csv(EE_path+'/EE_TimeSeries.csv')
       
       Th_TimeSeries[s] = {}
       
       for c in range(nC):
    
           Th_TimeSeries[s][c] = pd.concat([Th_Demand.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Lost_Load.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_SC_Prod.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Boiler_Prod.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Tank_Outflow.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Curtailment.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Th_Resist_En.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], Tank_SoC.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:], NG_Cons.iloc[(s*c*nP+c*nP):(s*c*nP+c*nP+nP),:]], axis=1)
           Th_TimeSeries[s][c].columns = ['Demand','Lost Load', 'SC production', 'Boiler production', 'Tank Outflow', 'Curtailment', 'Resistance Energy', 'Tank SoC', 'NG consumption']
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
    RES_Units = instance.RES_Units.get_values()[None]
    RES_Specific_Capacity = instance.RES_Nominal_Capacity.extract_values()[None]
    RES_Capacity = pd.DataFrame(['RES', 'kW', RES_Units*RES_Specific_Capacity/1000]).T.set_index([0,1])
    
    Bat_Capacity = pd.DataFrame(['Battery', 'kWh', instance.Battery_Nominal_Capacity.get_values()[None]/1000]).T.set_index([0,1])
       
    Gen_Capacity = pd.DataFrame(['Genset', 'kW', instance.Generator_Nominal_Capacity.get_values()[None]/1000]).T.set_index([0,1])
    
    EE_system = pd.concat([RES_Capacity,Bat_Capacity,Gen_Capacity], axis=0)
    EE_system.index.names = ['EE components', 'Unit']
    EE_system.columns = ['Total']

    
    # Thermal system components
    Boiler_Capacity = list(instance.Boiler_Nominal_Capacity.get_values().values())
    Boiler_Capacity = [i/1000 for i in Boiler_Capacity]
    Boiler_Capacity = pd.DataFrame([['NG Boiler', 'kW'] + Boiler_Capacity]).set_index([0,1])
    
    SC_Units = list(instance.SC_Units.get_values().values())
    SC_Specific_Capacity = instance.SC_Nominal_Capacity.extract_values()[None]
    SC_Capacity = [i*SC_Specific_Capacity/1000 for i in SC_Units]
    SC_Capacity = pd.DataFrame([['SC', 'kW'] + SC_Capacity]).set_index([0,1])
    
    Tank_Capacity = list(instance.Tank_Nominal_Capacity.get_values().values())
    Tank_Capacity = [i/1000 for i in Tank_Capacity]
    Tank_Capacity = pd.DataFrame([['Tank', 'kW'] + Tank_Capacity]).set_index([0,1])
        
    Resistance_Power = list(instance.Resistance_Nominal_Power.get_values().values())
    Resistance_Power = [i/1000 for i in Resistance_Power]
    Resistance_Power = pd.DataFrame([['Electric resistance', 'kW'] + Resistance_Power]).set_index([0,1])
    
    Th_system = pd.concat([SC_Capacity,Boiler_Capacity,Tank_Capacity,Resistance_Power, ], axis=0)
    Th_system = pd.concat([Th_system, Th_system.sum(1).to_frame()],axis=1)
    Th_system.index.names = ['Th Components', 'Unit']
    Th_system.columns = ['Class'+str(c+1) for c in range(nC)]+['Total']
    
    EnergySystemSize = pd.concat([EE_system, Th_system],axis=0).fillna("-")
    


    #%% Economic analysis
    NPC = pd.DataFrame(['Net Present Cost', 'MUSD', instance.ObjectiveFuntion.expr()/1e6]).T.set_index([0,1])
    NPC.columns = ['Total']
    
    #%% Investment cost   
    RES_Specific_Investment_Cost = instance.RES_Investment_Cost.extract_values()[None]
    RES_Investment_Cost = pd.DataFrame(['Investment Cost', 'RES', 'MUSD', RES_Units*RES_Specific_Investment_Cost/1e6]).T.set_index([0,1,2])
    RES_Investment_Cost.columns = ['Total']
    
    Bat_Capacity = instance.Battery_Nominal_Capacity.get_values()[None]
    Bat_Specific_Investment_Cost = instance.Battery_Invesment_Cost.extract_values()[None]
    Bat_Investment_Cost = pd.DataFrame(['Investment Cost', 'Battery', 'MUSD', Bat_Capacity*Bat_Specific_Investment_Cost/1e6]).T.set_index([0,1,2])
    Bat_Investment_Cost.columns = ['Total']

    Gen_Capacity = instance.Generator_Nominal_Capacity.get_values()[None]
    Gen_Specific_Investment_Cost = instance.Generator_Invesment_Cost.extract_values()[None]
    Gen_Investment_Cost = pd.DataFrame(['Investment Cost', 'Genset', 'MUSD', Gen_Capacity*Gen_Specific_Investment_Cost/1e6]).T.set_index([0,1,2])
    Gen_Investment_Cost.columns = ['Total']
    
    SC_Specific_Investment_Cost = instance.SC_Investment_Cost.extract_values()[None]
    SC_Capacity = [i*SC_Specific_Capacity for i in SC_Units]
    SC_Investment_Cost = pd.DataFrame(np.multiply(SC_Capacity, SC_Specific_Investment_Cost/1e6)).T
    SC_Investment_Cost = pd.concat([pd.DataFrame(['Investment Cost', 'SC', 'MUSD']).T,SC_Investment_Cost], axis=1)
    SC_Investment_Cost.columns = np.arange(SC_Investment_Cost.shape[1])
    SC_Investment_Cost = SC_Investment_Cost.set_index([0,1,2])

    Tank_Specific_Investment_Cost = instance.Tank_Invesment_Cost.extract_values()[None]
    Tank_Capacity = list(instance.Tank_Nominal_Capacity.get_values().values())
    Tank_Investment_Cost = pd.DataFrame(np.multiply(Tank_Capacity, Tank_Specific_Investment_Cost/1e6)).T 
    Tank_Investment_Cost = pd.concat([pd.DataFrame(['Investment Cost', 'Tank', 'MUSD']).T,Tank_Investment_Cost], axis=1)
    Tank_Investment_Cost.columns = np.arange(Tank_Investment_Cost.shape[1])
    Tank_Investment_Cost = Tank_Investment_Cost.set_index([0,1,2])

    Boiler_Specific_Investment_Cost = instance.Boiler_Invesment_Cost.extract_values()[None]
    Boiler_Capacity = list(instance.Boiler_Nominal_Capacity.get_values().values())
    Boiler_Investment_Cost = pd.DataFrame(np.multiply(Boiler_Capacity, Boiler_Specific_Investment_Cost/1e6)).T 
    Boiler_Investment_Cost = pd.concat([pd.DataFrame(['Investment Cost', 'NG Boiler', 'MUSD']).T,Boiler_Investment_Cost], axis=1)
    Boiler_Investment_Cost.columns = np.arange(Boiler_Investment_Cost.shape[1])
    Boiler_Investment_Cost = Boiler_Investment_Cost.set_index([0,1,2])

    Resistance_Specific_Investment_Cost = instance.Resistance_Invesment_Cost.extract_values()[None]
    Resistance_Power = list(instance.Resistance_Nominal_Power.get_values().values())
    Resistance_Investment_Cost = pd.DataFrame(np.multiply(Resistance_Power, Resistance_Specific_Investment_Cost/1e6)).T 
    Resistance_Investment_Cost = pd.concat([pd.DataFrame(['Investment Cost', 'Electric resistance', 'MUSD']).T,Resistance_Investment_Cost], axis=1)
    Resistance_Investment_Cost.columns = np.arange(Resistance_Investment_Cost.shape[1])
    Resistance_Investment_Cost = Resistance_Investment_Cost.set_index([0,1,2])


    #%% O&M cost   
    RES_OM_Cost = pd.DataFrame()
    Bat_OM_Cost = pd.DataFrame()
    Gen_OM_Cost = pd.DataFrame()
    SC_OM_Cost = pd.DataFrame()
    Tank_OM_Cost = pd.DataFrame()
    Boiler_OM_Cost = pd.DataFrame()
    Resistance_OM_Cost = pd.DataFrame()
    
    for y in range(1,nY+1):
        RES_OM_Cost = pd.concat([RES_OM_Cost, pd.DataFrame(['O&M Cost', str(y),'RES', 'MUSD', RES_Units*instance.RES_Nominal_Capacity.extract_values()[None]*instance.RES_Investment_Cost.extract_values()[None]*instance.RES_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y]).T.set_index([0,1,2,3])],axis=0)
        Bat_OM_Cost = pd.concat([Bat_OM_Cost, pd.DataFrame(['O&M Cost', str(y),'Battery', 'MUSD', instance.Battery_Nominal_Capacity.extract_values()[None]*instance.Battery_Invesment_Cost.extract_values()[None]*instance.Battery_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y]).T.set_index([0,1,2,3])],axis=0)
        Gen_OM_Cost = pd.concat([Gen_OM_Cost, pd.DataFrame(['O&M Cost', str(y),'Genset', 'MUSD', instance.Generator_Nominal_Capacity.extract_values()[None]*instance.Generator_Invesment_Cost.extract_values()[None]*instance.Generator_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y]).T.set_index([0,1,2,3])],axis=0)
        
        SC_OM_Cost = pd.concat([SC_OM_Cost, pd.concat([pd.DataFrame(['O&M Cost', str(y),'SC', 'MUSD']).T, pd.DataFrame([i*instance.SC_Nominal_Capacity.extract_values()[None]*instance.SC_Investment_Cost.extract_values()[None]*instance.SC_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y for i in SC_Units]).T],axis=1)],axis=0)
        Tank_OM_Cost = pd.concat([Tank_OM_Cost, pd.concat([pd.DataFrame(['O&M Cost', str(y),'Tank', 'MUSD']).T, pd.DataFrame([i*instance.Tank_Invesment_Cost.extract_values()[None]*instance.Tank_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y for i in instance.Tank_Nominal_Capacity.extract_values()]).T],axis=1)],axis=0)
        Boiler_OM_Cost = pd.concat([Boiler_OM_Cost, pd.concat([pd.DataFrame(['O&M Cost', str(y),'NG Boiler', 'MUSD']).T, pd.DataFrame([i*instance.Boiler_Invesment_Cost.extract_values()[None]*instance.Boiler_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y for i in instance.Boiler_Nominal_Capacity.extract_values()]).T],axis=1)],axis=0)
        Resistance_OM_Cost = pd.concat([Resistance_OM_Cost, pd.concat([pd.DataFrame(['O&M Cost', str(y),'Electric resistance', 'MUSD']).T, pd.DataFrame([i*instance.Resistance_Invesment_Cost.extract_values()[None]*instance.Resistance_Maintenance_Operation_Cost.extract_values()[None]/1e6/(1+dr)**y for i in instance.Resistance_Nominal_Power.extract_values()]).T],axis=1)],axis=0)
        
    RES_OM_Cost.columns = ['Total']
    Bat_OM_Cost.columns = ['Total']
    Gen_OM_Cost.columns = ['Total']
    
    SC_OM_Cost.columns = np.arange(SC_OM_Cost.shape[1])        
    SC_OM_Cost = SC_OM_Cost.set_index([0,1,2,3])
    SC_OM_Cost.columns = ['Class'+str(c+1) for c in range(nC)]
    
    Tank_OM_Cost.columns = np.arange(Tank_OM_Cost.shape[1])        
    Tank_OM_Cost = Tank_OM_Cost.set_index([0,1,2,3])
    Tank_OM_Cost.columns = ['Class'+str(c+1) for c in range(nC)]
    
    Boiler_OM_Cost.columns = np.arange(Boiler_OM_Cost.shape[1])        
    Boiler_OM_Cost = Boiler_OM_Cost.set_index([0,1,2,3])
    Boiler_OM_Cost.columns = ['Class'+str(c+1) for c in range(nC)]
    
    Resistance_OM_Cost.columns = np.arange(Resistance_OM_Cost.shape[1])        
    Resistance_OM_Cost = Resistance_OM_Cost.set_index([0,1,2,3])
    Resistance_OM_Cost.columns = ['Class'+str(c+1) for c in range(nC)]
    
   



    #%% Concatenating
    EE_Inv_Cost = pd.concat([RES_Investment_Cost, Bat_Investment_Cost, Gen_Investment_Cost], axis=0)
    EE_Inv_Cost.index.names = ['Cost item', 'Component', 'Unit']
    
    Th_Inv_Cost = pd.concat([SC_Investment_Cost, Boiler_Investment_Cost, Tank_Investment_Cost, Resistance_Investment_Cost], axis=0)
    Th_Inv_Cost.index.names = ['Cost item', 'Component', 'Unit']
    Th_Inv_Cost = pd.concat([Th_Inv_Cost, Th_Inv_Cost.sum(1).to_frame()],axis=1)      
    Th_Inv_Cost.columns = ['Class'+str(c+1) for c in range(nC)]+['Total']

    EE_OM_Cost = pd.concat([RES_OM_Cost, Bat_OM_Cost, Gen_OM_Cost], axis=0).groupby(level=[0,2,3],axis=0,sort=False).sum()
    EE_OM_Cost.index.names = ['Cost item', 'Component', 'Unit']
    
    Th_tot_OM_Cost = pd.concat([SC_OM_Cost, Boiler_OM_Cost, Tank_OM_Cost, Resistance_OM_Cost], axis=0).groupby(level=[0,2,3],axis=0,sort=False).sum()
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

    

