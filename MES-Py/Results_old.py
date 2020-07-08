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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick

import warnings
warnings.filterwarnings("ignore")


#%%
def Load_results1(instance):
    '''
    This function loads the results that depend of the periods in to a dataframe and creates a excel file with it.
    
    :param instance: The instance of the project resolution created by PYOMO.
    
    :return: A dataframe called Time_series with the values of the variables that depend of the periods.    
    '''
    
    # Load the variables that depend of the periods in python dyctionarys a
    
    
    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Periods = int(instance.Periods.extract_values()[None])
    
    #Scenarios = [[] for i in range(Number_Scenarios)]
    
    columns = []
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))

    #columns=columns
    Scenarios = pd.DataFrame()
    
     
    Lost_Load_EE = instance.Lost_Load_EE.get_values()
    PV_Energy = instance.Total_RES_Energy_Production.get_values()
    Battery_Flow_Out = instance.Energy_Battery_Flow_Out.get_values()
    Battery_Flow_in = instance.Energy_Battery_Flow_In.get_values()
    Curtailment = instance.Electric_Energy_Curtailment.get_values()
    Electric_Energy_Demand = instance.Electric_Energy_Demand.extract_values()
    SOC = instance.Battery_State_of_Charge.get_values()
    Gen_Energy = instance.Total_Generator_Energy_Production.get_values()
    Diesel = instance.Diesel_Consumption.get_values()
   
    
    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
    
    for i in range(0,Number_Scenarios):
        for j in range(1, Number_Periods+1):
            Scenarios_Periods[i].append((i+1,j))
    foo=0        
    for i in columns:
        Information = [[] for i in range(9)]
        for j in  Scenarios_Periods[foo]:
            Information[0].append(Lost_Load_EE[j])
            Information[1].append(PV_Energy[j]) 
            Information[2].append(Battery_Flow_Out[j]) 
            Information[3].append(Battery_Flow_in[j]) 
            Information[4].append(Curtailment[j]) 
            Information[5].append(Electric_Energy_Demand[j]) 
            Information[6].append(SOC[j])
            Information[7].append(Gen_Energy[j])
            Information[8].append(Diesel[j])
        
        Scenarios=Scenarios.append(Information)
        foo+=1
    
    index=[]  
    for j in range(1, Number_Scenarios+1):   
       index.append('Lost_Load_EE '+str(j))
       index.append('PV_Energy '+str(j))
       index.append('Battery_Flow_Out '+str(j)) 
       index.append('Battery_Flow_in '+str(j))
       index.append('Curtailment '+str(j))
       index.append('Electric_Energy_Demand '+str(j))
       index.append('SOC '+str(j))
       index.append('Gen energy '+str(j))
       index.append('Diesel '+str(j))
    Scenarios.index= index
     

     # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
    
    Scenarios.columns = columns
    Scenarios = Scenarios.transpose()
    
    Scenarios.to_csv('Results/Time_Series.csv') # Creating an excel file with the values of the variables that are in function of the periods
    
    columns = [] # arreglar varios columns
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))
        
    Scenario_information =[[] for i in range(Number_Scenarios)]
    Scenario_NPC = instance.Scenario_Net_Present_Cost.get_values()
    LoL_Cost = instance.Scenario_Lost_Load_Cost_EE.get_values() 
    Scenario_Weight = instance.Scenario_Weight.extract_values()
    Diesel_Cost = instance.Total_Diesel_Cost.get_values()
    
    for i in range(1, Number_Scenarios+1):
        Scenario_information[i-1].append(Scenario_NPC[i])
        Scenario_information[i-1].append(LoL_Cost[i])
        Scenario_information[i-1].append(Scenario_Weight[i])
        Scenario_information[i-1].append(Diesel_Cost[i])
    
    
    Scenario_Information = pd.DataFrame(Scenario_information,index=columns)
    Scenario_Information.columns=['Scenario NPC', 'LoL Cost','Scenario Weight', 'Diesel Cost']
    Scenario_Information = Scenario_Information.transpose()
    
    Scenario_Information.to_csv('Results/Scenario_Information.csv')
    
    S = instance.PlotScenario.value
    Time_Series = pd.DataFrame(index=range(0,Number_Periods))
    Time_Series.index = Scenarios.index
    
    Time_Series['Lost Load'] = Scenarios['Lost_Load_EE '+str(S)]
    Time_Series['Energy PV'] = Scenarios['PV_Energy '+str(S)]
    Time_Series['Discharge energy from the Battery'] = Scenarios['Battery_Flow_Out '+str(S)] 
    Time_Series['Charge energy to the Battery'] = Scenarios['Battery_Flow_in '+str(S)]
    Time_Series['Curtailment'] = Scenarios['Curtailment '+str(S)]
    Time_Series['Electric_Energy_Demand'] = Scenarios['Electric_Energy_Demand '+str(S)]
    Time_Series['Battery_State_of_Charge'] = Scenarios['SOC '+str(S)]
    Time_Series['Energy Diesel'] = Scenarios['Gen energy '+str(S)]
    Time_Series['Diesel'] = Scenarios['Diesel '+str(S)]    
    
    return Time_Series,Scenarios




#%% 
def Load_Thermal_Results1(instance):
    
    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Classes = int(instance.Classes.extract_values()[None])
    Number_Periods = int(instance.Periods.extract_values()[None])

    colonne=[]
    
    for k in range (1,Number_Scenarios+1):
        colonne.append('Scenarios_'+str(k))

    columns= []

    for i in range (1,Number_Classes+1):
        columns.append('Classes_'+str(i))

    Scenarios_Classes=pd.DataFrame()
    
    Lost_Load_Th = instance.Lost_Load_Th.get_values()
    SC_Energy = instance.Total_SC_Energy_Production.get_values()
    Energy_Tank_Flow_Out = instance.Energy_Tank_Flow_Out.get_values()
    Thermal_Curtailment = instance.Thermal_Energy_Curtailment.get_values()
    # Thermal_Energy_Demand = instance.Total_Thermal_Energy_Demand.get_values() # sostituito extract_values con get_values
    Thermal_Energy_Demand = instance.Thermal_Energy_Demand.extract_values() 
    Tank_State_of_Charge = instance.Tank_State_of_Charge.get_values()
    Total_Boiler_Energy_Production = instance.Total_Boiler_Energy_Production.get_values()
    NaturalGas = instance.NG_Consumption.get_values()
    Resistance = instance.Resistance_Thermal_Energy.get_values()
    Scenarios_Classes_Periods = [[] for i in range (Number_Classes*Number_Scenarios)]

    for k in range (0,Number_Scenarios):
        for i in range(0,Number_Classes):
            for j in range(1, Number_Periods+1):
                Scenarios_Classes_Periods[Number_Classes*k+i].append((k+1,i+1,j))

    foo=0     
    for k in colonne:
        for i in columns:
            Information = [[] for i in range(9)]
            for j in  Scenarios_Classes_Periods[foo]:
                Information[0].append(SC_Energy[j])
                Information[1].append(Energy_Tank_Flow_Out[j])
                Information[2].append(Thermal_Curtailment[j])
                Information[3].append(Thermal_Energy_Demand[j])
                Information[4].append(Tank_State_of_Charge[j])
                Information[5].append(Total_Boiler_Energy_Production[j])
                Information[6].append(NaturalGas[j])
                Information[7].append(Resistance[j])
                Information[8].append(Lost_Load_Th[j])
                                
            Scenarios_Classes=Scenarios_Classes.append(Information)
            foo+=1
                
        index=[]  
        for i in range (1,Number_Scenarios+1):
            for j in range(1, Number_Classes+1):   
                index.append('SC_Energy '+str(i)+','+str(j))
                index.append('Tank_Flow_Out '+str(i)+','+str(j))
                index.append('Thermal_Curtailment '+str(i)+','+str(j))
                index.append('Thermal_Energy_Demand '+str(i)+','+str(j))
                index.append('Tank_State_of_Charge '+str(i)+','+str(j))
                index.append('Total_Boiler_Energy_Production '+str(i)+','+str(j))
                index.append('NaturalGas '+str(i)+','+str(j))
                index.append('Resistance '+str(i)+','+str(j))
                index.append('Lost_Load_Th '+str(j)+','+str(j))
                
        Scenarios_Classes.index= index
                        

     # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
        
    Scenarios_Classes.columns=columns
    Scenarios_Classes=Scenarios_Classes.transpose()
        
    Scenarios_Classes.to_csv('Results/Time_Series_Thermal.csv') # Creating an excel file with the values of the variables that are in function of the periods

    return Scenarios_Classes



#%%
def Load_results2(instance):
    '''
    This function extracts the unidimensional variables into a  data frame and creates a excel file with it.
    this data
    
    :param instance: The instance of the project resolution created by PYOMO. 
    
    :return: Data frame called Size_variables with the variables values. 
    '''
    # Load the variables that doesnot depend of the periods in python dyctionarys
    ca = instance.Loan_Financial_Cost.get_values()
    cb = instance.RES_Units.get_values()
    cb=instance.RES_Nominal_Capacity.value*cb[None]
    cc = instance.Battery_Nominal_Capacity.get_values()
    NPC = instance.ObjectiveFuntion.expr()
    Funded= instance.Percentage_Funded.value
    DiscountRate = instance.Discount_Rate.value
    InterestRate = instance.Interest_Rate_Loan.value
    PricePV = instance.RES_Invesment_Cost.value
    PriceBattery= instance.Battery_Invesment_Cost.value
    OM = instance.RES_Maintenance_Operation_Cost.value
    Years=instance.Years.value
    Gen_cap = instance.Generator_Nominal_Capacity.get_values()[None]
    Diesel_Cost = instance.Diesel_Unitary_Cost.value
    Pricegen = instance.Generator_Invesment_Cost.value 
    Initial_Investment_Cost = instance.Initial_Investment_Cost.get_values()[None]
    O_M_Cost = instance.Operation_Maintenance_Cost.get_values()[None]
    Total_Financial_Cost = instance.Total_Financial_Cost.get_values()[None]
    Battery_Replacement_Cost = instance.Battery_Replacement_Cost.get_values()[None]
    VOLL = instance.Value_Of_Lost_Load.value
    
    
    
    data3 = np.array([ca[None],cb,cc[None],NPC,Funded, DiscountRate, InterestRate,
                      PricePV, PriceBattery, OM, Years, Initial_Investment_Cost,
                      O_M_Cost, Total_Financial_Cost, Battery_Replacement_Cost, VOLL,
                      Gen_cap, Diesel_Cost, Pricegen]) # Loading the values to a numpy array
    index_values = ['Amortization', 'Size of the solar panels', 'Size of the Battery',
                    'NPC','% Financimiento', 'Discount Rate', 'Interest Rate', 
                    'Price PV', 'Price Battery', 'OyM', 'Years', 'Initial Inversion', 
                    'O&M', 'Total Financial Cost','Battery Reposition Cost','VOLL', 
                    'Size Generator', 'Diesel Cost','Price Generator']
    # Create a data frame for the variable that don't depend of the periods of analisys 
    Size_variables = pd.DataFrame(data3,index=index_values)
    Size_variables.to_csv('Results/Size.csv') # Creating an excel file with the values of the variables that does not depend of the periods
    
    return Size_variables


#%%    
def Plot_Energy_Total(instance, Time_Series):  
    '''
    This function creates a plot of the dispatch of energy of a defined number of days.
    
    :param instance: The instance of the project resolution created by PYOMO. 
    :param Time_series: The results of the optimization model that depend of the periods.
    
    
    '''
    Periods_Day = 24/instance.Delta_Time() # periods in a day
    for x in range(0, instance.Periods()): # Find the position form wich the plot will start in the Time_Series dataframe
        foo = pd.DatetimeIndex(start=instance.PlotDay(),periods=1,freq='1h') # Asign the start date of the graphic to a dumb variable
        if foo == Time_Series.index[x]: 
           Start_Plot = x # asign the value of x to the position where the plot will start 
    End_Plot = Start_Plot + instance.PlotTime()*Periods_Day # Create the end of the plot position inside the time_series
    
    
    Time_Series.index=range(1,Time_Series.shape[0]+1)
    
    # Time_Series.index=range(1,35041)
    Plot_Data = Time_Series[Start_Plot:int(End_Plot)] # Extract the data between the start and end position from the Time_Series
    columns = pd.DatetimeIndex(start=instance.PlotDay(), periods=instance.PlotTime()*Periods_Day, freq=('1h'))    
    Plot_Data.index=columns
    
    
    Vec = pd.Series(Plot_Data['Energy PV'].values + Plot_Data['Energy Diesel'].values - Plot_Data['Curtailment'].values - Plot_Data['Charge energy to the Battery'].values , index=Plot_Data.index) # Create a vector with the sum of the diesel and solar energy
    Vec2 = pd.Series(Plot_Data['Electric_Energy_Demand'].values + Plot_Data['Curtailment'].values + Plot_Data['Charge energy to the Battery'].values, index=Plot_Data.index ) # Solar super plus of energy
    
    Vec3 = pd.Series(Vec.values + Plot_Data['Discharge energy from the Battery'].values, index=Plot_Data.index) # Substracction between the demand and energy discharge from the battery 
    Vec4 = -Plot_Data['Charge energy to the Battery'] # Creating a vector with the negative values of the energy going to the battery 
    Vec5 = pd.Series(Plot_Data['Electric_Energy_Demand'].values - Plot_Data['Lost Load'].values, index=Plot_Data.index)    
    
    ax1= Vec.plot(style='b-', linewidth=0.0) # Plot the line of the diesel energy plus the PV energy
#    pylab.ylim([-2000000,10000000])
    ax1.fill_between(Plot_Data.index, Plot_Data['Energy Diesel'].values, Vec.values,   alpha=0.3, color = 'b') # Fill the are of the energy produce by the energy of the PV
    ax2= Plot_Data['Energy Diesel'].plot(style='r', linewidth=0.5) # Plot the line of the diesel energy
    ax2.fill_between(Plot_Data.index, 0, Plot_Data['Energy Diesel'].values, alpha=0.2, color='r') # Fill the area of the energy produce by the diesel generator
    ax3= Plot_Data.Electric_Energy_Demand.plot(style='k-',linewidth=1) # Plot the line of the Electric_Energy_Demand
    ax3.fill_between(Plot_Data.index, Vec.values , Vec3.values, alpha=0.3, color='g') # Fill the area of the energy flowing out the battery
    ax5= Vec4.plot(style='m', linewidth=0.5) # Plot the line of the energy flowing into the battery
    ax5.fill_between(Plot_Data.index, 0, Vec4, alpha=0.3, color='m') # Fill the area of the energy flowing into the battery
    ax6= Plot_Data['Battery_State_of_Charge'].plot(style='k--', secondary_y=True, linewidth=2, alpha=0.7 ) # Plot the line of the State of charge of the battery
#    pylab.ylim([0,10000000])
    ax7= Vec2.plot(style='b-', linewidth=0.0) # Plot the line of PV energy that exceeds the demand
    ax7.fill_between(Plot_Data.index, Plot_Data['Electric_Energy_Demand'].values, Vec2.values,  alpha=0.3, color = 'b') # Fill the area between the demand and the curtailment energy
    ax3.fill_between(Plot_Data.index, Vec5 , Plot_Data['Electric_Energy_Demand'].values, alpha=0.3, color='y') 
    
    # Define name  and units of the axis
    ax1.set_ylabel('Power (W)')
    ax1.set_xlabel('Time (Hours)')
    ax6.set_ylabel('Battery State of charge (Wh)')
    
    # Define the legends of the plot
    From_PV = mpatches.Patch(color='blue',alpha=0.3, label='From PV')
    From_Generator = mpatches.Patch(color='red',alpha=0.3, label='From Generator')
    From_Battery = mpatches.Patch(color='green',alpha=0.5, label='From Battery')
    To_Battery = mpatches.Patch(color='magenta',alpha=0.5, label='To Battery')
    Lost_Load = mpatches.Patch(color='yellow', alpha= 0.3, label= 'Lost Load')
    Electric_Energy_Demand = mlines.Line2D([], [], color='black',label='Electric_Energy_Demand')
    Battery_State_of_Charge = mlines.Line2D([], [], color='black',label='Battery_State_of_Charge', linestyle='--',alpha=0.7)
    plt.legend(handles=[From_Generator, From_PV, From_Battery, To_Battery, Lost_Load, Electric_Energy_Demand, Battery_State_of_Charge], bbox_to_anchor=(1.83, 1))
    plt.savefig('Results/Energy_Dispatch.png', bbox_inches='tight')    
    plt.show()    
    
def Percentage_Of_Use(Time_Series):
    '''
    This model creates a plot with the percentage of the time that each technologies is activate during the analized 
    time.
    :param Time_series: The results of the optimization model that depend of the periods.
    '''    
    
    # Creation of the technolgy dictonary    
    PercentageOfUse= {'Lost Load':0, 'Energy PV':0,'Curtailment':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Charge energy to the Battery':0}
    
    # Count the quantity of times each technology has energy production
    for v in PercentageOfUse.keys():
        foo = 0
        for i in range(len(Time_Series)):
            if Time_Series[v][i]>0: 
                foo = foo + 1      
            PercentageOfUse[v] = (round((foo/float(len(Time_Series))), 3))*100 
    
    # Create the names in the plot
    c = ['From Generator', 'Curtailment', 'To Battery', 'From PV', 'From Battery', 'Lost Load']       
    
#     Create the bar plot  
    plt.figure()
    plt.bar((1,2,3,4,5,6), PercentageOfUse.values(), color= 'b', alpha=0.5, align='center')
   
    plt.xticks((1.2,2.2,3.2,4.2,5.2,6.2), c) # Put the names and position for the ticks in the x axis 
    plt.xticks(rotation=-30) # Rotate the ticks
    plt.xlabel('Technology') # Create a label for the x axis
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.ylabel('Percentage of use (%)') # Create a label for the y axis
    plt.savefig('Results/Percentge_of_Use.png', bbox_inches='tight') # Save the plot 
    plt.show() 
    
    return PercentageOfUse
    
def Energy_Flow(Time_Series):


    Energy_Flow = {'Electric_Energy_Demand':0, 'Lost Load':0, 'Energy PV':0,'Curtailment':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Charge energy to the Battery':0}

    for v in Energy_Flow.keys():
        if v == 'Energy PV':
            Energy_Flow[v] = round((Time_Series[v].sum() - Time_Series['Curtailment'].sum()- Time_Series['Charge energy to the Battery'].sum())/1000000, 2)
        else:
            Energy_Flow[v] = round((Time_Series[v].sum())/1000000, 2)
          
    
    c = ['From Generator', 'To Battery', 'Demand', 'From PV', 'From Battery', 'Curtailment', 'Lost Load']       
    plt.figure()    
    plt.bar((1,2,3,4,5,6,7), Energy_Flow.values(), color= 'b', alpha=0.3, align='center')
    
    plt.xticks((1.2,2.2,3.2,4.2,5.2,6.2,7.2), c)
    plt.xlabel('Technology')
    plt.ylabel('Energy Flow (MWh)')
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='on')
    plt.xticks(rotation=-30)
    plt.savefig('Results/Energy_Flow.png', bbox_inches='tight')
    plt.show()    
    
    return Energy_Flow

def Energy_Participation(Energy_Flow):
    
    Energy_Participation = {'Energy PV':0, 'Energy Diesel':0, 'Discharge energy from the Battery':0, 'Lost Load':0}
    c = {'Energy Diesel':'Diesel Generator', 'Discharge energy from the Battery':'Battery', 'Energy PV':'From PV', 'Lost Load':'Lost Load'}       
    labels=[]
    
    for v in Energy_Participation.keys():
        if Energy_Flow[v]/Energy_Flow['Electric_Energy_Demand'] >= 0.001:
            Energy_Participation[v] = Energy_Flow[v]/Energy_Flow['Electric_Energy_Demand']
            labels.append(c[v])
        else:
            del Energy_Participation[v]
    Colors=['r','c','b','k']
    
    plt.figure()                     
    plt.pie(Energy_Participation.values(), autopct='%1.1f%%', colors=Colors)
    
    Handles = []
    for t in range(len(labels)):
        Handles.append(mpatches.Patch(color=Colors[t], alpha=1, label=labels[t]))
    
    plt.legend(handles=Handles, bbox_to_anchor=(1.4, 1))   
    plt.savefig('Results/Energy_Participation.png', bbox_inches='tight')
    plt.show()
    
    return Energy_Participation

def LDR(Time_Series):

    columns=['Consume diesel', 'Lost Load', 'Energy PV','Curtailment','Energy Diesel', 
             'Discharge energy from the Battery', 'Charge energy to the Battery', 
             'Electric_Energy_Demand',  'Battery_State_of_Charge'  ]
    Sort_Values = Time_Series.sort('Electric_Energy_Demand', ascending=False)
    
    index_values = []
    
    for i in range(len(Time_Series)):
        index_values.append((i+1)/float(len(Time_Series))*100)
    
    Sort_Values = pd.DataFrame(Sort_Values.values/1000, columns=columns, index=index_values)
    
    plt.figure() 
    ax = Sort_Values['Electric_Energy_Demand'].plot(style='k-',linewidth=1)
    
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    ax.set_ylabel('Load (kWh)')
    ax.set_xlabel('Percentage (%)')
    
    plt.savefig('Results/LDR.png', bbox_inches='tight')
    plt.show()    