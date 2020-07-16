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


from pyomo.opt import SolverFactory
from pyomo.environ import Objective, minimize, Constraint


from Constraints import  Net_Present_Cost, Loan_Financial_Cost, Electric_Energy_balance, Maximum_Lost_Load_EE, Maximun_Lost_Load_Th,\
Scenario_Net_Present_Cost, Scenario_Lost_Load_Cost_EE, Scenario_Lost_Load_Cost_Th, Initial_Investment_Cost, Operation_Maintenance_Cost,\
Total_Financial_Cost, Maximum_Diesel_Energy, Diesel_Comsuption,Total_Diesel_Cost, Maximum_Boiler_Energy,\
NG_Consumption, Thermal_Energy_Balance, Boiler_Financial_Cost , Total_NG_Cost


def Model_Resolution(model,datapath="Inputs/data.dat"):   
    
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    :param datapath: path to the input data file
    
    :return: The solution inside an object called instance.
    '''
    
    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Electric_Energy_balance)
    model.MaximunLostLoad = Constraint(model.scenario, rule=Maximum_Lost_Load_EE) # Maximum permissible lost load
    model.MaximunLostLoadTh = Constraint(model.scenario, model.classes, rule=Maximun_Lost_Load_Th) # Maximum permissible lost load
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost_EE)
    model.ScenarioLostLoadCostTh = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost_Th)
    model.ThermalEnergyBalance = Constraint(model.scenario, model.classes, model.periods, rule=Thermal_Energy_Balance)
    
    # Boiler Constraints     
    model.MaximumBoilerEnergy = Constraint(model.scenario, model.classes, model.periods, rule =Maximum_Boiler_Energy) 
    model.NGConsumption = Constraint(model.scenario, model.classes, model.periods, rule = NG_Consumption)
    model.NGCostTotal = Constraint(model.scenario, rule = Total_NG_Cost)
        
    # Diesel Generator constraints
    model.MaximumDieselEnergy = Constraint(model.scenario, model.periods, rule=Maximum_Diesel_Energy) # Maximum energy output of the diesel generator
    model.DieselComsuption = Constraint(model.scenario, model.periods, rule=Diesel_Comsuption)    # Diesel comsuption 
    model.DieselCostTotal = Constraint(model.scenario, rule=Total_Diesel_Cost)
    
    # Financial Constraints
    #model.MinRES = Constraint(model.scenario, model.classes, rule = Min_Renewables )
    model.BoilerFinancialCost = Constraint(rule =Boiler_Financial_Cost )
    model.FinancialCost = Constraint(rule=Loan_Financial_Cost)
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost)    
    model.InitialInversion = Constraint(rule=Initial_Investment_Cost)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Financial_Cost)

    
    print('Model_Resolution: Constraints imported')
    
    instance = model.create_instance(datapath) # load parameters

    print('Model_Resolution: Instance created')
    
    opt = SolverFactory('gurobi')# # Solver use during the optimization    
    opt.set_options('Method=2 Crossover=0 BarConvTol=1e-4 OptimalityTol=1e-4 FeasibilityTol=1e-4 IterationLimit=1000')
	
    print('Model_Resolution: Solver called')
    
    results = opt.solve(instance, tee=True)# Solving a model instance 
    
    print('Model_Resolution: instance solved')

    instance.solutions.load_from(results)  # Loading solution into instance
    return instance

    