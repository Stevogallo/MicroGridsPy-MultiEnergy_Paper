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

from pyomo.environ import  Param, RangeSet, NonNegativeReals, Var

from Initialize import Initialize_years, Initialize_Electric_Energy_Demand, Initialize_Thermal_Energy_Demand # Import library with initialitation funtions for the parameters


def Model_Creation(model):
    '''
    This function creates the instance for the resolution of the optimization in Pyomo.
    :param model: Pyomo model as defined in the Micro-Grids library
    '''
    
    # Time parameters
    model.Periods = Param(within=NonNegativeReals)  # Number of periods per year of analysis of the energy variables
    model.Years = Param()                           # Number of years of the project
   
    # Configuration parameters
    model.Scenarios = Param()                       # Number of scenarios
    model.Classes = Param(within=NonNegativeReals)  # Number of classes of users for the thermal part
    
    # Plot parameters
    model.StartDate = Param()                       # Start date of the project
    model.PlotTime = Param()                        # Quantity of days that are going to be plot
    model.PlotDay = Param()                         # Start day for the plot
    model.PlotScenario = Param()                    # Scenario for the plot
        
    # SETS
    model.periods = RangeSet(1, model.Periods)      # Creation of a set from 1 to the number of periods in each year
    model.years = RangeSet(1, model.Years)          # Creation of a set from 1 to the number of years of the project
    model.scenario = RangeSet(1, model.Scenarios)   # Creation of a set from 1 to the numbero scenarios to analized
    model.classes = RangeSet(1, model.Classes)      # Creation of a set from 1 to the number of classes of the thermal part
    
    #%% PARAMETERS
            
    # Parametes of the diesel generator
    model.Generator_Efficiency = Param()        # Generator electric efficiency in %
    model.Lower_Heating_Value  = Param()        # Lower heating value of the diesel in Wh/L
    model.Diesel_Unitary_Cost  = Param(within=NonNegativeReals)     # Cost of diesel in USD/L
    model.Generator_Invesment_Cost = Param(within=NonNegativeReals) # Investment cost of the diesel generator in USD/W
    model.Generator_Maintenance_Operation_Cost = Param(within=NonNegativeReals) # % of the total investment spend in operation and management of diesel generator in each period
    
    # Parameters of the Boiler 
    model.Boiler_Efficiency = Param()       # Boiler efficiency in %
    model.Lower_Heating_Value_NG = Param()  # Lower heating value of the natural gas in Wh/L
    model.NG_Unitary_Cost = Param(within=NonNegativeReals)       # Cost of natural gas in USD/L
    model.Boiler_Invesment_Cost = Param(within=NonNegativeReals) # Investment cost of the NG Boiler in USD/W
    model.Boiler_Maintenance_Operation_Cost = Param (within=NonNegativeReals) # % of the total investment spend in operation and management of boiler in each period
    
    # Parameters of the Energy balance                  
    model.Electric_Energy_Demand = Param(model.scenario, model.periods, initialize=Initialize_Electric_Energy_Demand) # Electric Energy_Demand in W 
    model.Lost_Load_Tolerance = Param(within=NonNegativeReals)      # Fraction of tolerated lost load in % of the total demand
    model.Value_Of_Lost_Load = Param(within=NonNegativeReals)       # Value of lost load in USD/Wh
    model.Thermal_Energy_Demand = Param(model.scenario, model.classes, model.periods, initialize=Initialize_Thermal_Energy_Demand) # Thermal Energy Demand in W 
    
    # Parameters of the project
    model.Delta_Time = Param(within=NonNegativeReals)                           # Time step in hours
    model.Percentage_Funded = Param(within=NonNegativeReals)                    # % of the total investment that is funded by a bank or another entity in %
    model.Project_Years = Param(model.years, initialize= Initialize_years)      # Years of the project
    model.Discount_Rate = Param()                                               # Discount rate of the project in %
    model.Interest_Rate_Loan = Param()                                          # Interest rate of the loan in %
    model.Scenario_Weight = Param(model.scenario, within=NonNegativeReals)      # Probability of occurrance of each scenario
    
    #%% VARIABLES
            
    # Variables associated to the diesel generator
    model.Generator_Nominal_Capacity = Var(within=NonNegativeReals)                          # Capacity  of the diesel generator in Wh
    model.Diesel_Consumption = Var(model.scenario,model.periods, within=NonNegativeReals)    # Diesel consumed to produce electric energy in L
    model.Total_Generator_Energy_Production = Var(model.scenario, model.periods, within=NonNegativeReals)     # Total Energy production from the Diesel generator
    model.Total_Diesel_Cost = Var(model.scenario, within=NonNegativeReals)
    
    ## Variables associated to the Boiler 
    model.Boiler_Nominal_Capacity = Var (model.classes, within=NonNegativeReals)                     # Capacity of the boiler in Wh
    model.NG_Consumption = Var(model.scenario, model.classes, model.periods,within=NonNegativeReals) # Natural Gas consumed to produce thermal energy in Kg (considering Liquified Natural Gas)
    model.Total_Boiler_Energy_Production = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy generated by the boiler 
    model.Total_NG_Cost = Var(model.scenario, within=NonNegativeReals) 
    
    # Varialbles associated to the energy balance
    model.Lost_Load_EE = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy not suply by the system Wh
    model.Lost_Load_Th = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy not suply by the system Wh
    model.Electric_Energy_Curtailment = Var(model.scenario, model.periods, within=NonNegativeReals) # Curtailment of RES energy in Wh
    model.Scenario_Lost_Load_Cost_EE = Var(model.scenario, within=NonNegativeReals) ####
    model.Scenario_Lost_Load_Cost_Th = Var(model.scenario, within=NonNegativeReals) ####
    model.Thermal_Energy_Curtailment = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals)

    # Variables associated to the financial costs
    model.Boiler_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Boiler technology considering all the classes
    
    # Variables associated to the project
    model.Loan_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of each period in USD
    model.Scenario_Net_Present_Cost = Var(model.scenario, within=NonNegativeReals) ####
    model.Initial_Investment_Cost = Var(within=NonNegativeReals)
    model.Operation_Maintenance_Cost = Var(within=NonNegativeReals)
    model.Total_Financial_Cost = Var(within=NonNegativeReals)
    
    