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

from pyomo.environ import  Param, RangeSet, NonNegativeReals, Var
from Initialize import Initialize_years, Initialize_Electric_Energy_Demand, Initialize_RES_Energy, Initialize_SC_Energy, Initialize_Thermal_Energy_Demand # Import library with initialitation funtions for the parameters

## Thermal Model ##

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
    # Renewable Energy Source parameters
    model.RES_Nominal_Capacity = Param(within=NonNegativeReals)     # Nominal capacity of the RES in W/unit
    model.RES_Inverter_Efficiency = Param()                         # Efficiency of the inverter in %
    model.RES_Invesment_Cost = Param(within=NonNegativeReals)       # Investment cost of RES unit in USD/W
    model.RES_Maintenance_Operation_Cost = Param(within=NonNegativeReals) # % of the total investment spend in operation and management of RES unit in each period                                             
    model.RES_Energy_Production = Param(model.scenario, model.periods, within=NonNegativeReals, initialize=Initialize_RES_Energy) # Energy production of a RES unit in W    
    
    # Solare Collectors parameters
    model.SC_Nominal_Capacity = Param(within=NonNegativeReals) # Nominal capacity of the Solar Collectors in W
    model.SC_Investment_Cost = Param(within=NonNegativeReals)  # Investment cost of SC in USD/W
    model.SC_Maintenance_Operation_Cost = Param(within=NonNegativeReals)    # % of the total investment spend in operation and management of SC unit in each period   
    model.SC_Energy_Production = Param (model.scenario, model.classes, model.periods, within=NonNegativeReals, initialize=Initialize_SC_Energy)  # Energy production of a SC unit in W 

    # Parameters of the battery bank
    model.Charge_Battery_Efficiency = Param()        # Efficiency of the charge of the battery in  %
    model.Discharge_Battery_Efficiency = Param()     # Efficiency of the discharge of the battery in %
    model.Battery_Depth_of_Discharge = Param()       # Depth of discharge of the battery in %
    model.Maximum_Battery_Charge_Time = Param(within=NonNegativeReals)        # Maximum time of charge of the battery in hours
    model.Maximum_Battery_Discharge_Time = Param(within=NonNegativeReals)     # Maximum time of discharge of the battery  in hours                     
    model.Battery_Replacement_Time = Param(within=NonNegativeReals)           # Period of replacement of the battery in years
    model.Battery_Invesment_Cost = Param(within=NonNegativeReals)             # Investment cost of battery in USD/Wh
    model.Battery_Maintenance_Operation_Cost = Param(within=NonNegativeReals) # % of the total investment spend in operation and management of battery unit in each period
    
    # Parameters of the tank storage 
    model.Tank_Efficiency = Param()                                           # Efficiency of the tank %   
    model.Tank_Depth_of_Discharge = Param ()                                  # Depth of discharge of the tank in %
    model.Maximum_Tank_Discharge_Time = Param (within=NonNegativeReals)       # Maximum time of discharge of the tank in hours
    model.Tank_Invesment_Cost = Param(within=NonNegativeReals)                # Investment cost of unit tank USD/W
    model.Tank_Maintenance_Operation_Cost = Param (within=NonNegativeReals)   # % of the total investment spend in operation and management of tank unit in each period
    
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

    # Parameters of the Electric Resistance  
    model.Electric_Resistance_Efficiency = Param()                                # Electric resistance efficiency in %
    model.Resistance_Invesment_Cost = Param(within=NonNegativeReals)              # Investment cost of the electric resistance in USD/W
    model.Resistance_Maintenance_Operation_Cost = Param (within=NonNegativeReals) # % of the total investment spend in operation and management of resistance in each period
    
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
    # Variables associated to the RES
    model.RES_Units = Var(within=NonNegativeReals)                                                  # Number of units of RES
    model.Total_RES_Energy_Production = Var(model.scenario,model.periods, within=NonNegativeReals)  # Total energy generated for the RES system in Wh
    model.SC_Units = Var(model.classes,within=NonNegativeReals)                                     # Number of units of solar collector
    model.Total_SC_Energy_Production = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Total energy generated by solar collectors in Wh

    # Variables associated to the battery bank
    model.Battery_Nominal_Capacity = Var(within=NonNegativeReals)                               # Capacity of the battery bank in Wh
    model.Energy_Battery_Flow_Out = Var(model.scenario, model.periods, within=NonNegativeReals) # Battery discharge energy in Wh
    model.Energy_Battery_Flow_In = Var(model.scenario, model.periods, within=NonNegativeReals)  # Battery charge energy in Wh
    model.Battery_State_of_Charge = Var(model.scenario, model.periods, within=NonNegativeReals) # State of Charge of the Battery in Wh
    model.Maximum_Battery_Charge_Power= Var()                                                           # Maximum charge power in W
    model.Maximum_Battery_Discharge_Power = Var()                                                       # Maximum discharge power in W
    model.Battery_Replacement_Cost = Var(within=NonNegativeReals)
    
    # Variables associated to the storage TANK
    model.Tank_Nominal_Capacity = Var(model.classes, within=NonNegativeReals)                               # Capacity of the tank in Wh
    model.Energy_Tank_Flow_Out = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Tank unit discharge energy in Wh
    model.Tank_State_of_Charge = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # State of Charge of the Tank in wh
    model.Maximum_Tank_Discharge_Power = Var(model.classes)
    
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
    
    # Variables associated to the RESISTANCE
    model.Resistance_Nominal_Power = Var(model.classes, within=NonNegativeReals)                    # Electric Nominal power of the thermal resistance 
    model.Resistance_Thermal_Energy = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Total Electric power considering all the users in each class
    model.Total_Electrical_Resistance_Demand = Var(model.scenario,model.periods, within=NonNegativeReals) # Total Resistance Energy required by the electrical supply considered in the electric energy balance
    
    # Varialbles associated to the energy balance
    model.Lost_Load_EE = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy not suply by the system Wh
    model.Lost_Load_Th = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy not suply by the system Wh
    model.Electric_Energy_Curtailment = Var(model.scenario, model.periods, within=NonNegativeReals) # Curtailment of RES energy in Wh
    model.Scenario_Lost_Load_Cost_EE = Var(model.scenario, within=NonNegativeReals) ####
    model.Scenario_Lost_Load_Cost_Th = Var(model.scenario, within=NonNegativeReals) ####
    model.Thermal_Energy_Curtailment = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals)

    # Variables associated to the financial costs
    model.SC_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of SC technology considering all the classes
    model.Tank_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Tank technology considering all the classes (he investment tank costs include the resistance cost)
    model.Boiler_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Boiler technology considering all the classes
    model.Resistance_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of Boiler technology considering all the classes
    
    # Variables associated to the project
    model.Loan_Financial_Cost = Var(within=NonNegativeReals) # Financial cost of each period in USD
    model.Scenario_Net_Present_Cost = Var(model.scenario, within=NonNegativeReals) ####
    model.Initial_Investment_Cost = Var(within=NonNegativeReals)
    model.Operation_Maintenance_Cost = Var(within=NonNegativeReals)
    model.Total_Financial_Cost = Var(within=NonNegativeReals)
    
    