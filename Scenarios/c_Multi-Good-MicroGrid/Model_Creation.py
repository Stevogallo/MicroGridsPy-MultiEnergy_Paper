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


from pyomo.environ import  Param, RangeSet, NonNegativeReals, Var

from Initialize import Initialize_years, Initialize_Electric_Energy_Demand, Initialize_Thermal_Energy_Demand, Initialize_RES_Energy # Import library with initialitation funtions for the parameters


def Model_Creation(model):
    
    "Time parameters"
    model.Periods = Param(within=NonNegativeReals)  # Number of periods per year of analysis of the energy variables
    model.Years = Param()                           # Number of years of the project
   
    "Configuration parameters"
    model.Scenarios = Param()                       # Number of scenarios
    model.Classes = Param(within=NonNegativeReals)  # Number of classes of users for the thermal part
    
    "Plot parameters"
    model.StartDate = Param()                       # Start date of the project
    model.PlotTime = Param()                        # Quantity of days that are going to be plot
    model.PlotDay = Param()                         # Start day for the plot
    model.PlotScenario = Param()                    # Scenario for the plot
        
    "SETS"
    model.periods = RangeSet(1, model.Periods)      # Creation of a set from 1 to the number of periods in each year
    model.years = RangeSet(1, model.Years)          # Creation of a set from 1 to the number of years of the project
    model.scenario = RangeSet(1, model.Scenarios)   # Creation of a set from 1 to the numbero scenarios to analized
    model.classes = RangeSet(1, model.Classes)      # Creation of a set from 1 to the number of classes of the thermal part

    
    #%% System parameters

    "Parameters of the RES"
    model.RES_Nominal_Capacity = Param(within=NonNegativeReals)     # Nominal capacity of the RES in W/unit
    model.RES_Inverter_Efficiency = Param()                         # Efficiency of the inverter in %
    model.RES_Inv_Specific_Cost = Param(within=NonNegativeReals)    # Investment cost of RES unit in USD/W
    model.RES_OM_Specific_Cost = Param(within=NonNegativeReals)     # % of the total investment spent in operation and management of RES unit in each period                                             
    model.RES_Unit_Energy_Production = Param(model.scenario, model.periods, within=NonNegativeReals, initialize=Initialize_RES_Energy) # Energy production of a RES unit in W    

    "Parameters of the battery bank"
    model.BESS_Discharge_Efficiency = Param()        # Efficiency of the charge of the battery in  %
    model.BESS_Charge_Efficiency = Param()           # Efficiency of the discharge of the battery in %
    model.BESS_Depth_of_Discharge = Param()          # Depth of discharge of the battery in %
    model.BESS_Maximum_Discharge_Time = Param(within=NonNegativeReals)        # Maximum time of charge of the battery in hours
    model.BESS_Maximum_Charge_Time = Param(within=NonNegativeReals)           # Maximum time of discharge of the battery  in hours                     
    model.BESS_Replacement_Time = Param(within=NonNegativeReals)              # Period of replacement of the battery in years
    model.BESS_Inv_Specific_Cost = Param(within=NonNegativeReals)            # Investment cost of battery in USD/Wh
    model.BESS_OM_Specific_Cost = Param(within=NonNegativeReals)              # % of the total investment spend in operation and management of battery unit in each period
            
    "Parameters of the diesel generator"
    model.Generator_Efficiency = Param()        # Generator electric efficiency in %
    model.Lower_Heating_Value  = Param()        # Lower heating value of the diesel in Wh/L
    model.Diesel_Unitary_Cost  = Param(within=NonNegativeReals)        # Cost of diesel in USD/L
    model.Generator_Inv_Specific_Cost = Param(within=NonNegativeReals) # Investment cost of the diesel generator in USD/W
    model.Generator_OM_Specific_Cost  = Param(within=NonNegativeReals) # % of the total investment spent in operation and management of diesel generator in each period
    
    "Parameters of the electric resistance"
    model.Electric_Resistance_Efficiency = Param()                               # Electric resistance efficiency in %
    model.Electric_Resistance_Specific_Inv_Cost = Param(within=NonNegativeReals) # Investment cost of the electric resistance in USD/W
    model.Electric_Resistance_OM_Specific_Cost = Param(within=NonNegativeReals)  # % of the total investment spent in operation and management of electric resistance in each period
    
    "Parameters of the Energy balance"                  
    model.Electric_Energy_Demand = Param(model.scenario, model.periods, initialize=Initialize_Electric_Energy_Demand) # Electric Energy_Demand in W 
    model.EE_Lost_Load_Tolerance = Param(within=NonNegativeReals)      # Fraction of tolerated lost load in % of the total demand
    model.EE_Value_Of_Lost_Load = Param(within=NonNegativeReals)       # Value of lost load in USD/Wh
    
    model.Thermal_Energy_Demand = Param(model.scenario, model.classes, model.periods, initialize=Initialize_Thermal_Energy_Demand) # Thermal Energy Demand in W 
    model.Th_Lost_Load_Tolerance = Param(within=NonNegativeReals)      # Fraction of tolerated lost load in % of the total demand
    model.Th_Value_Of_Lost_Load = Param(within=NonNegativeReals)       # Value of lost load in USD/Wh
    
    "Parameters of the project"
    model.Delta_Time = Param(within=NonNegativeReals)                           # Time step in hours
    model.Project_Years = Param(model.years, initialize= Initialize_years)      # Years of the project
    model.Discount_Rate = Param()                                               # Discount rate of the project in %
    model.Scenario_Weight = Param(model.scenario, within=NonNegativeReals)      # Probability of occurrance of each scenario

    
    #%% System variables

    "Variables associated to the RES"
    model.RES_Units = Var(within=NonNegativeReals)                                            # Number of units of RES
    model.RES_Energy_Production = Var(model.scenario,model.periods, within=NonNegativeReals)  # Total energy generated for the RES system in Wh
    model.RES_Investment_Cost = Var(within=NonNegativeReals)                                  # Total investment cost of the RES in USD    
    model.RES_OM_Cost = Var(within=NonNegativeReals)                                          # Total fixed OM cost of the RES in USD    

    "Variables associated to the battery bank"
    model.BESS_Nominal_Capacity = Var(within=NonNegativeReals)                                # Capacity of the battery bank in Wh
    model.BESS_Outflow = Var(model.scenario, model.periods, within=NonNegativeReals)          # Battery outflow in Wh
    model.BESS_Inflow = Var(model.scenario, model.periods, within=NonNegativeReals)           # Battery inflow energy in Wh
    model.BESS_State_of_Charge = Var(model.scenario, model.periods, within=NonNegativeReals)  # State of Charge of the battery in Wh
    model.Maximum_BESS_Charge_Power= Var(within=NonNegativeReals)                             # Maximum charge power in W
    model.Maximum_BESS_Discharge_Power = Var(within=NonNegativeReals)                      # Maximum discharge power in W
    model.BESS_Investment_Cost = Var(within=NonNegativeReals)                                 # Total investment cost of the batteries in USD 
    model.BESS_OM_Cost = Var(within=NonNegativeReals)                                         # Total fixed OM cost of the batteries in USD        
    model.BESS_Replacement_Cost = Var(within=NonNegativeReals)                                # Battery replacement cost
            
    "Variables associated to the diesel generator"
    model.Generator_Nominal_Capacity = Var(within=NonNegativeReals)                          # Capacity of the diesel generator in Wh
    model.Generator_Investment_Cost = Var(within=NonNegativeReals)                           # Total investment cost of the diesel generator in USD    
    model.Generator_OM_Cost = Var(within=NonNegativeReals)                                   # Total fixed OM cost of the diesel generator in USD    
    model.Diesel_Consumption = Var(model.scenario,model.periods, within=NonNegativeReals)    # Diesel consumed to produce electric energy in L
    model.Generator_Energy_Production = Var(model.scenario, model.periods, within=NonNegativeReals)     # Total Energy production from the Diesel generator
    model.Total_Diesel_Cost = Var(model.scenario, within=NonNegativeReals)
    
    "Variables associated to the electric resistance"
    model.Electric_Resistance_Nominal_Power = Var(model.classes, within=NonNegativeReals)    # Nominal power of the electric resistance in W
    model.Electric_Resistance_Investment_Cost = Var(model.classes, within=NonNegativeReals)  # Total investment cost of the electric resistance in USD
    model.Electric_Resistance_OM_Cost = Var(model.classes, within=NonNegativeReals)          # Total fixed OM cost of the electric resistance in USD
    model.Electric_Resistance_Energy_Consumption = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy consumed by the electric resistance in each class in Wh 
    model.Electric_Resistance_Energy_Production = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals)  # Energy generated by the electric resistance in each class in Wh 
    model.Tot_Electric_Resistance_Energy_Production = Var(model.scenario, model.periods, within=NonNegativeReals)            # Total energy generated by the electric resistance in Wh 
    
    "Varialbles associated to the energy balance"
    model.Lost_Load_EE = Var(model.scenario, model.periods, within=NonNegativeReals) # Energy not suply by the system Wh
    model.Lost_Load_Th = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals) # Energy not suply by the system Wh
    model.Electric_Curtailment = Var(model.scenario, model.periods, within=NonNegativeReals) # Curtailment of RES energy in Wh
    model.Scenario_Lost_Load_Cost_EE = Var(model.scenario, within=NonNegativeReals) ####
    model.Scenario_Lost_Load_Cost_Th = Var(model.scenario,model.classes, within=NonNegativeReals) 
    model.Thermal_Energy_Curtailment = Var(model.scenario, model.classes, model.periods, within=NonNegativeReals)
    
    "Variables associated to the project"
    model.Scenario_Net_Present_Cost = Var(model.scenario, within=NonNegativeReals) 
    model.Total_Investment_Cost = Var(within=NonNegativeReals)
    model.Fixed_Costs = Var(within=NonNegativeReals)
    model.Variable_Costs = Var(model.scenario, within=NonNegativeReals)
    
    