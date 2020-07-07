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

import warnings
warnings.filterwarnings("ignore")

#%% Objective funtion

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the sum of the multiplication of the net present cost 
    NPC (USD) of each scenario and their probability of occurrence.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
      
    return (sum(model.Scenario_Net_Present_Cost[i]*model.Scenario_Weight[i] for i in model.scenario ))

      
#%% RES constraints

def RES_Electric_Energy_Generation(model,i,t): # Total energy output of the RES system
    '''
    This constraint calculates the energy produce by the RES system taking in 
    account the efficiency of the inverter for each scenario.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_RES_Energy_Production[i,t] == model.RES_Energy_Production[i,t]*model.RES_Inverter_Efficiency*model.RES_Units


#%% SC constraints

def Solar_Thermal_Energy_Generation (model,i,c,t): # Energy output of solar collectors

    '''
    This constraint calculates the energy produced by the solar collectors 
    for each scenario considering all the users for each class (indicated by the parameter "c")
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_SC_Energy_Production[i,c,t] == model.SC_Energy_Production[i,c,t]*model.SC_Units[c]

def SC_Financial_Cost(model):
   '''
   This constraint defines the financial cost of the solar collector technology 
   as the summation of each class that will be considered in the Financial Cost. 
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.SC_Financial_Cost == sum(model.SC_Units[c]*model.SC_Investment_Cost*model.SC_Nominal_Capacity for c in model.classes)

#%% Battery constraints

def Battery_State_of_Charge(model,i,t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery (State_Of_Charge) 
    for each period of analysis. The State_Of_Charge is in the period 't' is equal to
    the State_Of_Charge in period 't-1' plus the energy flow into the battery, 
    minus the energy flow out of the battery. This is done for each scenario i.
    In time t=1 the Battery_State_of_Charge is equal to a fully charged battery.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    if t==1: # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.Battery_State_of_Charge[i,t] == model.Battery_Nominal_Capacity*1 - model.Energy_Battery_Flow_Out[i,t]*model.Delta_Time/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[i,t]*model.Delta_Time*model.Charge_Battery_Efficiency
    if t>1:  
        return model.Battery_State_of_Charge[i,t] == model.Battery_State_of_Charge[i,t-1] - model.Energy_Battery_Flow_Out[i,t]*model.Delta_Time/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[i,t]*model.Delta_Time*model.Charge_Battery_Efficiency    

def Maximum_Battery_Charge(model,i,t): # Maximum state of charge of the Battery
    '''
    This constraint keeps the state of charge of the battery equal or under the 
    size of the battery for each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Battery_State_of_Charge[i,t] <= model.Battery_Nominal_Capacity

def Minimum_Battery_Charge(model,i,t): # Minimum state of charge
    '''
    This constraint maintains the level of charge of the battery above the deep 
    of discharge in each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Battery_State_of_Charge[i,t] >= model.Battery_Nominal_Capacity*model.Battery_Depth_of_Discharge

def Max_Power_Battery_Charge(model): 
    '''
    This constraint calculates the Maximum power of charge of the battery. Taking in account the 
    capacity of the battery and a time frame in which the battery has to be fully loaded for 
    each scenario.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximum_Battery_Charge_Power == model.Battery_Nominal_Capacity/(model.Maximum_Battery_Charge_Time)

def Max_Power_Battery_Discharge(model):
    '''
    This constraint calculates the Maximum power of discharge of the battery. for 
    each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximum_Battery_Discharge_Power == model.Battery_Nominal_Capacity/(model.Maximum_Battery_Discharge_Time)

def Max_Battery_Energy_Inflow(model,i,t): # Maximum inflow of energy for the charge fase
    '''
    This constraint maintains the energy in to the battery, below the maximum power 
    of charge of the battery for each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_In[i,t] <= model.Maximum_Battery_Charge_Power

def Min_Battery_Energy_Outflow(model,i,t):  # Minimum outflow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the maximum power of 
    discharge of the battery for each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_Out[i,t] <= model.Maximum_Battery_Discharge_Power

def Battery_Replacement_Cost(model):
    '''
    This funtion calculates the reposition of the battery after a stated time of use. 
    :param model: Pyomo model as defined in the Model_creation library.
    ''' 
    return model.Battery_Replacement_Cost == (model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost)/((1+model.Discount_Rate)**model.Battery_Replacement_Time)


#%% Tank constraints

def Tank_State_Of_Charge(model,i,c,t): # State of Charge (SOC) of the thermal storage (Tank)
    '''
     This constraint calculates the state of charge of the thermal storage (tank)
     for each period of analysis and for each class of users. It is an energy
     balance on the hot water storage tank unit in each period. The Tank_State_of_Charge 
     in the period 't' is equal to the Tank_State_of_Charge in the period 't-1' plus the energy
     flow into the tank, minus the energy flow out of the tank, plus the resistance heat, curtailment and losses. This is done for each
     class c and scenario i. In time t=1 the Tank_State_of_Charge is equal to a fully charged tank.
     :param model: Pyomo model as defined in the Model_creation library.
     '''
    if t==1: # Tank_State_of_Charge  for the period 0 is equal to the Tank size.
        return model.Tank_State_of_Charge[i,c,t] == model.Tank_Nominal_Capacity[c]*1 + model.Total_SC_Energy_Production[i,c,t]*model.Delta_Time + model.Resistance_Thermal_Energy[i,c,t]*model.Electric_Resistance_Efficiency*model.Delta_Time - model.Energy_Tank_Flow_Out[i,c,t]*model.Delta_Time 

    if t>1:  
        return model.Tank_State_of_Charge [i,c,t] == model.Tank_State_of_Charge[i,c,t-1]*model.Tank_Efficiency + model.Total_SC_Energy_Production[i,c,t]*model.Delta_Time + model.Resistance_Thermal_Energy[i,c,t]*model.Electric_Resistance_Efficiency*model.Delta_Time - model.Energy_Tank_Flow_Out[i,c,t]*model.Delta_Time 

def Maximun_Tank_Charge(model,i,c,t): # Maximum state of charge of the tank in terms of thermal energy
    '''
    This constraint keeps the state of charge of the tank equal or under the 
    size of the tank for each scenario i and each class c.
    :param model: Pyomo model as defined in the Model_creation library.    
    '''
    return model.Tank_State_of_Charge[i,c,t] <= model.Tank_Nominal_Capacity[c]

def Minimun_Tank_Charge(model,i,c,t): # Minimum state of charge of the tank in terms of thermal energy
    '''
    This constraint maintains the level of charge of the battery above the deep 
    of discharge in each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Tank_State_of_Charge [i,c,t] >= model.Tank_Nominal_Capacity[c]*model.Tank_Depth_of_Discharge

def Max_Power_Tank_Discharge(model,c):
    '''
    This constraint calculates the Maximum power of discharge of the tank. for 
    each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximum_Tank_Discharge_Power[c] == model.Tank_Nominal_Capacity[c]/(model.Maximum_Tank_Discharge_Time)

def Min_Tank_Energy_Outflow(model,i,c, t): # Minimum outflow of energy for the discharge fase
    '''
    This constraint maintains the energy from the tank, below the maximum power of 
    discharge of the battery for each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Tank_Flow_Out[i,c,t] <= model.Maximum_Tank_Discharge_Power[c]

def Tank_Financial_Cost (model):
   '''
   This constraint defines the financial cost of the tank technology 
   as the summation of each class that will be considered in the Financial Cost.
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.Tank_Financial_Cost == sum(model.Tank_Nominal_Capacity[c]*model.Tank_Invesment_Cost for c in model.classes)


#%% Electrical resistance costraints

def Maximum_Resistance_Thermal_Energy(model,i,c,t):
    '''
    This constraint calculates the total thermal energy produced by the electrical resistance
    for each scenario i and class c.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Resistance_Thermal_Energy[i,c,t] <= model.Resistance_Nominal_Power[c]

def Resistance_Financial_Cost (model):
   ''' 
   This constraint defines the financial cost of the resistance technology 
   as the summation of each class that will be considered in the Financial Cost.
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.Resistance_Financial_Cost == sum(model.Resistance_Nominal_Power[c]*model.Resistance_Invesment_Cost for c in model.classes)


#%% Natural gas boiler constraints 

def Maximum_Boiler_Energy(model,i,c,t): # Maximum energy output of the Boiler    
    '''
    This constraint ensures that the boiler will not exceed his nominal capacity 
    in each period in each scenario i and class c.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Boiler_Energy_Production[i,c,t] <= model.Boiler_Nominal_Capacity[c]

def NG_Consumption(model,i,c,t): # NG comsuption 
    '''
    This constraint transforms the energy produced by the boiler generator into 
    kg of natural gas in each scenario i and class c.
    This is done using the lower heating value (LHV)
    of the natural gas and the efficiency of the boiler.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.NG_Consumption[i,c,t] == model.Total_Boiler_Energy_Production[i,c,t]*model.Delta_Time / (model.Boiler_Efficiency*(model.Lower_Heating_Value_NG))

def Boiler_Financial_Cost (model):
   ''' 
   This constraint defines the financial cost of the boiler technology 
   as the summation of each class that will be considered in the Financial Cost.
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.Boiler_Financial_Cost == sum(model.Boiler_Nominal_Capacity[c]*model.Boiler_Invesment_Cost for c in model.classes)

def Total_NG_Cost (model,i):
    '''
    This constraint calculates the total cost due to the use of Natural Gas to generate 
    thermal energy in the boiler in each scenario i. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[] 
    for c in range (1,model.Classes+1): 
        for f in range(1,model.Periods+1):
            foo.append((i,c,f))
    return  model.Total_NG_Cost[i] == sum(((sum(model.NG_Consumption[i,c,t]*model.NG_Unitary_Cost for i,c,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)


#%% Diesel generator constraints

def Maximum_Diesel_Energy(model,i,t): # Maximun energy output of the diesel generator
    '''
    This constraint ensures that the generator will not exceed his nominal capacity 
    in each period in each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Generator_Energy_Production[i,t] <= model.Generator_Nominal_Capacity

def Diesel_Comsuption(model,i, t): # Diesel comsuption 
    '''
    This constraint transforms the energy produce by the diesel generator in to 
    liters of diesel in each scenario i.This is done using the low heating value
    of the diesel and the efficiency of the diesel generator.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Diesel_Consumption[i,t] == model.Total_Generator_Energy_Production[i,t]*model.Delta_Time/(model.Generator_Efficiency*(model.Lower_Heating_Value))
 
def Total_Diesel_Cost(model,i):
    '''
    This constraint calculates the total cost due to the use of diesel to generate 
    electricity in the generator in each scenario i. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
    return model.Total_Diesel_Cost[i] == sum(((sum(model.Diesel_Consumption[i,t]*model.Diesel_Unitary_Cost for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
                                                                                                                                     
                                                                 
#%% Thermal energy balance

def Thermal_Energy_Balance(model,i,c,t): # Thermal energy balance
     '''
     This costraint ensures the perfect match between the energy demand of the 
     system and the different sources to meet the thermal energy demand for each class c 
     and each scenario i
     :param model: Pyomo model as defined in the Model_creation library.
     '''
     return  model.Thermal_Energy_Demand[i,c,t] == model.Total_Boiler_Energy_Production[i,c,t]  + model.Energy_Tank_Flow_Out[i,c,t] - model.Thermal_Energy_Curtailment[i,c,t] + model.Lost_Load_Th[i,c,t]

def Total_Electrical_Resistance_Demand (model,i,t): # The summation of the electrical resistance demand of each class. 
     '''
     This constraint defines the electrical demand that comes from the 
     electrical resistance to satisfy the thermal demand. 
     This term is involved in the electrical energy balance.
     :param model: Pyomo model as defined in the Model_creation library.
     '''
     return model.Total_Electrical_Resistance_Demand[i,t] == sum(model.Resistance_Thermal_Energy[i,c,t] for c in model.classes)


#%% Electric energy balance 

def Electric_Energy_balance(model,i,t): # Electric Energy balance
    '''
    This constraint ensures the perfect match between the electric energy demand of the 
    system and the differents sources to meet the energy demand including 
    the electric resistance demand of thermal part each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Electric_Energy_Demand[i,t] == model.Total_RES_Energy_Production[i,t] + model.Total_Generator_Energy_Production[i,t] - model.Energy_Battery_Flow_In[i,t] + model.Energy_Battery_Flow_Out[i,t] + model.Lost_Load_EE[i,t] - model.Electric_Energy_Curtailment[i,t] - model.Total_Electrical_Resistance_Demand[i,t]

def Maximum_Lost_Load_EE(model,i): # Maximum tolerated electric lost load
    '''
    This constraint ensures that the ratio between the lost load and the energy 
    Demand does not exceeds the value of the permisible lost load each scenario i. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Lost_Load_Tolerance >= (sum(model.Lost_Load_EE[i,t] for t in model.periods)/sum(model.Electric_Energy_Demand[i,t] for t in model.periods))

def Maximun_Lost_Load_Th(model,i,c): # Maximum permissible lost load thermal
    '''
    This constraint ensures that the ratio between the lost load and the energy 
    Demand does not exceeds the value of the permisible lost load each scenario i and class c. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Lost_Load_Tolerance*sum(model.Thermal_Energy_Demand[i,c,t] for t in model.periods) >= sum(model.Lost_Load_Th[i,c,t] for t in model.periods)


#%% Energy system economic constraints

def Scenario_Net_Present_Cost(model, i): 
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    :param model: Pyomo model as defined in the Model_creation library.
    '''            
    return model.Scenario_Net_Present_Cost[i] == model.Initial_Investment_Cost + model.Operation_Maintenance_Cost + model.Total_Financial_Cost + model.Battery_Replacement_Cost + model.Scenario_Lost_Load_Cost_EE[i] + model.Scenario_Lost_Load_Cost_Th[i] + model.Total_Diesel_Cost[i] + model.Total_NG_Cost[i]

def Initial_Investment_Cost(model):
    '''
    This constraint calculates the initial inversion for the system. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Initial_Investment_Cost == (model.RES_Units*model.RES_Invesment_Cost*model.RES_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.SC_Financial_Cost + model.Tank_Financial_Cost + model.Boiler_Financial_Cost + model.Resistance_Financial_Cost )*(1-model.Percentage_Funded) 
                                                                 
def Operation_Maintenance_Cost(model):
    '''
    This funtion calculates the operation and maintenance for the system. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Operation_Maintenance_Cost == sum(((model.RES_Units*model.RES_Invesment_Cost*model.RES_Nominal_Capacity*model.RES_Maintenance_Operation_Cost + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Battery_Maintenance_Operation_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Generator_Maintenance_Operation_Cost + model.SC_Financial_Cost*model.SC_Maintenance_Operation_Cost + model.Tank_Financial_Cost*model.Tank_Maintenance_Operation_Cost + model.Boiler_Financial_Cost*model.Boiler_Maintenance_Operation_Cost + model.Resistance_Financial_Cost*model.Resistance_Maintenance_Operation_Cost)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
                                                                                       
def Scenario_Lost_Load_Cost_EE(model, i):
    '''
    This constraint calculates the cost due to the lost load in each scenario i. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
        
    return  model.Scenario_Lost_Load_Cost_EE[i] == sum(((sum(model.Lost_Load_EE[i,t]*model.Value_Of_Lost_Load*model.Delta_Time for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
 
def Scenario_Lost_Load_Cost_Th (model,i):
    '''
    This constraint calculates the total cost due to the use of Natural Gas to generate 
    thermal energy in the boiler in each scenario i. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[] 
    for c in range (1,model.Classes+1): 
        for f in range(1,model.Periods+1):
            foo.append((i,c,f))
    return  model.Scenario_Lost_Load_Cost_Th[i] == sum(((sum(model.Lost_Load_Th[i,c,t]*model.Value_Of_Lost_Load*model.Delta_Time for i,c,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
 
def Loan_Financial_Cost(model): 
    '''
    This constraint calculates the yearly payment for the borrow money.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Loan_Financial_Cost == ((model.RES_Units*model.RES_Invesment_Cost*model.RES_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.SC_Financial_Cost + model.Tank_Financial_Cost + model.Boiler_Financial_Cost + model.Resistance_Financial_Cost)*model.Percentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))
  
def Total_Financial_Cost(model):
    '''
    This funtion calculates the total financial cost of the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Total_Financial_Cost == sum((model.Loan_Financial_Cost/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
    
