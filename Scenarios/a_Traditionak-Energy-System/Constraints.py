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


#%% Objective funtion

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the sum of the multiplication of the net present cost 
    NPC (USD) of each scenario and their probability of occurrence.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
      
    return (sum(model.Scenario_Net_Present_Cost[i]*model.Scenario_Weight[i] for i in model.scenario ))

    
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
     return  model.Thermal_Energy_Demand[i,c,t] == model.Total_Boiler_Energy_Production[i,c,t] - model.Thermal_Energy_Curtailment[i,c,t] + model.Lost_Load_Th[i,c,t]


#%% Electric energy balance 

def Electric_Energy_balance(model,i,t): # Electric Energy balance
    '''
    This constraint ensures the perfect match between the electric energy demand of the 
    system and the differents sources to meet the energy demand including 
    the electric resistance demand of thermal part each scenario i.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Electric_Energy_Demand[i,t] == model.Total_Generator_Energy_Production[i,t] + model.Lost_Load_EE[i,t] - model.Electric_Energy_Curtailment[i,t]

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
    return model.Scenario_Net_Present_Cost[i] == model.Initial_Investment_Cost + model.Operation_Maintenance_Cost + model.Total_Financial_Cost + model.Scenario_Lost_Load_Cost_EE[i] + model.Scenario_Lost_Load_Cost_Th[i] + model.Total_Diesel_Cost[i] + model.Total_NG_Cost[i]

def Initial_Investment_Cost(model):
    '''
    This constraint calculates the initial inversion for the system. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Initial_Investment_Cost == (model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.Boiler_Financial_Cost)*(1-model.Percentage_Funded) 
                                                                 
def Operation_Maintenance_Cost(model):
    '''
    This funtion calculates the operation and maintenance for the system. 
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Operation_Maintenance_Cost == sum(((model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Generator_Maintenance_Operation_Cost + model.Boiler_Financial_Cost*model.Boiler_Maintenance_Operation_Cost)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
                                                                                       
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
    return model.Loan_Financial_Cost == ((model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.Boiler_Financial_Cost)*model.Percentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))
  
def Total_Financial_Cost(model):
    '''
    This funtion calculates the total financial cost of the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Total_Financial_Cost == sum((model.Loan_Financial_Cost/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
    
