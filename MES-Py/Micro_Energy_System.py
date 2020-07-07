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

import time
from pyomo.environ import AbstractModel
import warnings
warnings.filterwarnings("ignore")

from Results import Plot_Energy_Total, Load_results1, Load_results2, Load_Thermal_Results1, Percentage_Of_Use, Energy_Flow, Energy_Participation, LDR
from Model_Creation import Model_Creation
from Model_Resolution import Model_Resolution


start = time.time()


model = AbstractModel() # define type of optimization problem


# Optimization model
Model_Creation(model) # Creation of the Sets, parameters and variables.
instance = Model_Resolution(model) # Resolution of the instance
## Upload the resulst from the instance and saving it in excel files
Time_Series,Scenarios = Load_results1(instance) # Extract the results of energy from the instance and save it in a excel file 
Scenarios_Classes = Load_Thermal_Results1(instance)
Results = Load_results2(instance) # Save results into a excel file

# Post procesing tools
Plot_Energy_Total(instance, Time_Series)


#PercentageOfUse = Percentage_Of_Use(Time_Series) # Plot the percentage of use 
#Energy_Flow = Energy_Flow(Time_Series) # Plot the quantity of energy of each technology analized
#Energy_Participation = Energy_Participation(Energy_Flow)
#LDR(Time_Series)


# Calculation of the Levelized cost of energy
#LCOE = Levelized_Cost_Of_Energy(Time_Series, Results, instance) # Calculate the Levelized Cost of energy for the system analysis


# messages
#print 'Net present cost of the project is ' + str(round((instance.ObjectiveFuntion.expr()/1000000),2)) + ' millons of USD' # Print net present cost of the project 
#print 'The levelized cost of energy of the project is ' + str(round(LCOE, 3)) + ' USD/kWh' # Print the levilez cost of energy


end = time.time()
elapsed = end - start
print("\nTime: ",round(elapsed,0),"sec")

