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
import matplotlib.pyplot as plt


Electric_Energy_Demand = pd.read_csv('Electric_Demand.csv', index_col=0)/1000  # Import electricity demand

StartDate = '01/01/2017 00:00:00'
Electric_Energy_Demand.index = pd.DatetimeIndex(start=StartDate, periods=525600, freq='1min')


StartDatePlot = ['12/21/2017 00:00:00','03/21/2017 00:00:00','06/21/2017 00:00:00','09/23/2017 00:00:00'] # MM/DD/YY
EndDatePlot   = ['12/21/2017 23:59:59','03/21/2017 23:59:59','06/21/2017 23:59:59','09/23/2017 23:59:59']

y_Plot1 = Electric_Energy_Demand.loc[StartDatePlot[0]:EndDatePlot[0], :].values
y_Plot2 = Electric_Energy_Demand.loc[StartDatePlot[1]:EndDatePlot[1], :].values
y_Plot3 = Electric_Energy_Demand.loc[StartDatePlot[2]:EndDatePlot[2], :].values
y_Plot4 = Electric_Energy_Demand.loc[StartDatePlot[3]:EndDatePlot[3], :].values
x_Plot  = np.arange(len(y_Plot1))


plt.figure(figsize=(15,6))

plt.plot(x_Plot, y_Plot4, '#2e279d', label='Spring')
plt.plot(x_Plot, y_Plot1, '#4d80e4', label='Summer')
plt.plot(x_Plot, y_Plot2, '#46b3e6', label='Fall')
plt.plot(x_Plot, y_Plot3, '#dff6f0', label='Winter')

plt.ylabel('Power (kW)', fontsize=14)
plt.xlabel('Time (Hours)', fontsize=14)

plt.ylim(ymin=0)
plt.ylim(ymax=200)

plt.margins(x=0)
plt.margins(y=0)

plt.xticks([0,(4*60),(8*60),(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])#, fontsize=14)
# plt.yticks(fontsize=14)

plt.grid(True)
plt.legend(loc='upper left', fontsize='15', facecolor='white')

plt.savefig('ElectricLoadCurves.png', dpi=500)










