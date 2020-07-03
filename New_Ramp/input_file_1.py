# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:59:08 2018

@author: stevo
"""

#%% Definition of the inputs
'''
Data from Field Campaign Pistolese-Stevanato 2017
'''



from core import User, np
User_list = []


#Create new user classes
HI = User("high income",130,3)
User_list.append(HI)

LI = User("low income",202,3)
User_list.append(LI)

Rest = User("restaurants",6)
User_list.append(Rest)

Guest = User("guesthouses",4)
User_list.append(Guest)

Comm = User("commercialactivities",17)
User_list.append(Comm)

Doctor = User("doctor",1)
User_list.append(Doctor)
'''
School = User("school",1)
User_list.append(School)
'''
Cancha = User("cancha",1)
User_list.append(Cancha)

Public_lighting = User("public lighting",1)
User_list.append(Public_lighting)

Carabineros = User("policestation",1)
User_list.append(Carabineros)

#Create new appliances


#High-Income 

HI_indoor_bulb = HI.Appliance(HI,7,60,2,360,0.2,2)
HI_indoor_bulb.windows([1080,1440],[0,30],0.35)

HI_outdoor_bulb = HI.Appliance(HI,1,60,2,300,0.2,15)
HI_outdoor_bulb.windows([0,420],[1200,1440],0.35)

HI_TV = HI.Appliance(HI,3,150,2,360,0.1,30)
HI_TV.windows([540,780],[1080,1440],0.35)

HI_Radio = HI.Appliance(HI,1,7,2,240,0.1,30)
HI_Radio.windows([480,720],[1080,1380],0.35)

HI_Boiler = HI.Appliance(HI,1,1000,2,15,0.1,1)
HI_Boiler.windows([420,540],[960,1080],0.35)

HI_Phone_charger = HI.Appliance(HI,4,5,2,480,0.2,60)
HI_Phone_charger.windows([1200,1440],[0,420],0.35)

HI_Freezer = HI.Appliance(HI,1,250,1,1440,0,30,'yes',3)
HI_Freezer.windows([0,1440],[0,0])
HI_Freezer.specific_cycle_1(200,20,5,10)
HI_Freezer.specific_cycle_2(200,15,5,15)
HI_Freezer.specific_cycle_3(200,10,5,20)
HI_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

HI_Laptop = HI.Appliance(HI,1,70,1,90,0.1,30)
HI_Laptop.windows([960,1440],[0,0],0.35)

HI_Iron = HI.Appliance(HI,1,700,1,30,0.1,1,occasional_use = 0.28, thermal_P_var = 0.4)
HI_Iron.windows([600,1200],[0,0],0.35)

HI_WMachine = HI.Appliance(HI,1,500,1,60,0.1,occasional_use = 0.14)
HI_WMachine.windows([540,720],[0,0],0.35)
HI_WMachine.specific_cycle_1(500,5,5,20)
HI_WMachine.specific_cycle_2(400,5,5,30)
HI_WMachine.cycle_behaviour([540,600],[0,0],[600,720],[0,0])


#Low Income

LI_indoor_bulb = LI.Appliance(LI,5,60,2,300,0.2,10)
LI_indoor_bulb.windows([1080,1440],[0,30],0.35)

LI_outdoor_bulb = LI.Appliance(LI,1,60,2,60,0.2,30)
LI_outdoor_bulb.windows([0,420],[1200,1440],0.35)

LI_TV = LI.Appliance(LI,2,150,2,240,0.1,30)
LI_TV.windows([540,780],[1080,1440],0.35)

LI_Radio = LI.Appliance(LI,1,7,2,240,0.1,30)
LI_Radio.windows([480,720],[1080,1380],0.35)

LI_Boiler = LI.Appliance(LI,1,1000,2,10,0.1,1)
LI_Boiler.windows([420,540],[960,1080],0.35)

LI_Phone_charger = LI.Appliance(LI,2,5,2,360,0.2,10)
LI_Phone_charger.windows([1200,1440],[0,420],0.35)

LI_Freezer = LI.Appliance(LI,1,250,1,1440,0,30,'yes',3)
LI_Freezer.windows([0,1440],[0,0])
LI_Freezer.specific_cycle_1(200,20,5,10)
LI_Freezer.specific_cycle_2(200,15,5,15)
LI_Freezer.specific_cycle_3(200,10,5,20)
LI_Freezer.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

LI_Laptop = LI.Appliance(LI,1,70,1,60,0.1,30)
LI_Laptop.windows([960,1440],[0,0],0.35)

LI_Iron = LI.Appliance(LI,1,700,1,15,0.1,1,occasional_use = 0.2, thermal_P_var = 0.4)
LI_Iron.windows([600,1200],[0,0],0.35)

# Restaurants

Rest_indoor_bulb = Rest.Appliance(Rest,10,60,1,480,0.1,60)
Rest_indoor_bulb.windows([480,1380],[0,0],0.1)

Rest_outdoor_bulb = Rest.Appliance(Rest,2,60,1,200,0.1,30)
Rest_outdoor_bulb.windows([1100,1440],[0,0],0.1)

Rest_TV = Rest.Appliance(Rest,2,150,1,480,0.1,30)
Rest_TV.windows([600,1380],[0,0],0.1)

Rest_phone_charger = Rest.Appliance(Rest,2,5,1,240,0.1,30)
Rest_phone_charger.windows([600,1380],[0,0],0.1)

Rest_fridge = Rest.Appliance(Rest,5,250,1,1440,0,30,'yes',3)
Rest_fridge.windows([0,1440],[0,0])
Rest_fridge.specific_cycle_1(200,20,5,10)
Rest_fridge.specific_cycle_2(200,15,5,15)
Rest_fridge.specific_cycle_3(200,10,5,20)
Rest_fridge.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

Rest_water_boiler = Rest.Appliance(Rest,1,1000,1,40,0.2,1)
Rest_water_boiler.windows([600,1200],[0,0],0.15)

Rest_microwave = Rest.Appliance(Rest,1,700,1,40,0.2,2,thermal_P_var = 0.4)
Rest_microwave.windows([600,1200],[0,0],0.15)

# GuestHouses

Guest_indoor_bulb = Guest.Appliance(Guest,20,60,1,240,0.1,30)
Guest_indoor_bulb.windows([1080,1440],[0,0],0.1)

Guest_outdoor_bulb = Guest.Appliance(Guest,10,60,2,600,0.1,300)
Guest_outdoor_bulb.windows([1080,1440],[0,400],0.1)

Guest_TV = Guest.Appliance(Guest,5,150,1,300,0.1,20)
Guest_TV.windows([480,1440],[0,0],0.1)

Guest_phone_charger = Guest.Appliance(Guest,4,5,1,240,0.1,30)
Guest_phone_charger.windows([0,1440],[0,0],0)

Guest_fridge = Guest.Appliance(Guest,2,250,1,1440,0,30,'yes',3)
Guest_fridge.windows([0,1440],[0,0])
Guest_fridge.specific_cycle_1(200,20,5,10)
Guest_fridge.specific_cycle_2(200,15,5,15)
Guest_fridge.specific_cycle_3(200,10,5,20)
Guest_fridge.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

Guest_water_boiler = Guest.Appliance(Guest,1,1000,1,40,0.2,1)
Guest_water_boiler.windows([360,720],[0,0],0.15)

# Commercial Actvities

Comm_indoor_bulb = Comm.Appliance(Comm,8,60,1,480,0.1,60)
Comm_indoor_bulb.windows([480,1200],[0,0],0.1)

Comm_outdoor_bulb = Comm.Appliance(Comm,1,60,1,120,0.1,60)
Comm_outdoor_bulb.windows([1080,1200],[0,0],0.1)

Comm_TV = Comm.Appliance(Comm,1,150,1,600,0.1,120)
Comm_TV.windows([480,1200],[0,0],0.1)

Comm_Radio = Comm.Appliance(Comm,1,7,1,600,0.1,60)
Comm_Radio.windows([480,1200],[0,0],0.1)

Comm_phone_charger = Comm.Appliance(Comm,1,5,1,240,0.1,30)
Comm_phone_charger.windows([480,1200],[0,0],0.1)

Comm_fridge = Comm.Appliance(Comm,5,250,1,1440,0,30,'yes',3)
Comm_fridge.windows([0,1440],[0,0])
Comm_fridge.specific_cycle_1(200,20,5,10)
Comm_fridge.specific_cycle_2(200,15,5,15)
Comm_fridge.specific_cycle_3(200,10,5,20)
Comm_fridge.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

# Puesta Medica

Doctor_indoor_bulb = Doctor.Appliance(Doctor,10,60,1,600,0.1,30)
Doctor_indoor_bulb.windows([480,1200],[0,0],0.1)


Doctor_TV = Doctor.Appliance(Doctor,1,150,1,600,0.1,60)
Doctor_TV.windows([480,1200],[0,0],0.1)

Doctor_Radio = Doctor.Appliance(Doctor,1,7,1,180,0.1,20)
Doctor_Radio.windows([480,1200],[0,0],0.1)

Doctor_phone_charger = Doctor.Appliance(Doctor,3,4,1,120,0.1,30)
Doctor_phone_charger.windows([480,720],[0,0],0.1)

Doctor_fridge = Doctor.Appliance(Doctor,1,250,1,1440,0,30,'yes',3)
Doctor_fridge.windows([0,1440],[0,0])
Doctor_fridge.specific_cycle_1(200,20,5,10)
Doctor_fridge.specific_cycle_2(200,15,5,15)
Doctor_fridge.specific_cycle_3(200,10,5,20)
Doctor_fridge.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

Doctor_PC = Doctor.Appliance(Doctor,1,70,1,600,0.1,600)
Doctor_PC.windows([480,1200],[0,0],0.1)

Doctor_water_boiler = Doctor.Appliance(Doctor,1,1000,1,20,0.1,2)
Doctor_water_boiler.windows([480,1200],[0,0],0.1)

Doctor_autoclave = Doctor.Appliance(Doctor,1,120,1,120,0.1,120,occasional_use = 0.14,thermal_P_var = 0.3)
Doctor_autoclave.windows([480,1200],[0,0],0.1)

Doctor_dental_compressor = Doctor.Appliance(Doctor,1,550,1,180,0.1,60,occasional_use = 0.14, thermal_P_var = 0.2)
Doctor_dental_compressor.windows([480,1200],[0,0],0.1)

# School
'''
School_indoor_bulb = School.Appliance(School,60,60,1,480,0.1,30)
School_indoor_bulb.windows([480,1080],[0,0])

School_outdoor_bulb = School.Appliance(School,10,60,1,360,0.1,30)
School_outdoor_bulb.windows([480,1080],[0,0])

School_phone_charger = School.Appliance(School,40,5,1,240,0.1,30)
School_phone_charger.windows([480,1080],[0,0])

School_PC = School.Appliance(School,25,70,1,480,0.1,60)
School_PC.windows([480,1080],[0,0])

School_TV = School.Appliance(School,10,150,1,120,0.1,30)
School_TV.windows([480,1080],[0,0])

School_radio = School.Appliance(School,25,7,1,360,0.1,30)
School_radio.windows([480,1080],[0,0])

School_fridge = School.Appliance(School,8,250,1,1440,0,30,'yes',3)
School_fridge.windows([0,1440],[0,0])
School_fridge.specific_cycle_1(200,20,5,10)
School_fridge.specific_cycle_2(200,15,5,15)
School_fridge.specific_cycle_3(200,10,5,20)
School_fridge.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

School_water_boiler = School.Appliance(School,10,1000,1,120,0.1,2)
School_water_boiler.windows([480,1080],[0,0])
'''
# Public Lights

Lights = Public_lighting.Appliance(Public_lighting, 100, 150, 2, 600, 0.05, 600, flat = 'yes')
Lights.windows([1215,1440],[0,420],0.05)

# Cancha

Cancha_lights = Cancha.Appliance(Cancha,12,400,1,120,0.1,60, occasional_use=0.07)
Cancha_lights.windows([1215,1440],[0,0],0.05)

# Carabineros

Carabineros_indoor_lights = Carabineros.Appliance(Carabineros,12,60,1,360,0.1,10)
Carabineros_indoor_lights.windows([600,1200],[0,0],0.1)

Carabineros_outdoor_lights = Carabineros.Appliance(Carabineros,3,60,2,420,0.1,60)
Carabineros_outdoor_lights.windows([1380,1400],[0,420],0.1)

Carabineros_TV = Carabineros.Appliance(Carabineros,6,150,2,180,0.2,30)
Carabineros_TV.windows([600,720],[1080,1200],0.1)

Carabineros_radio = Carabineros.Appliance(Carabineros,1,7,1,360,0.1,5)
Carabineros_radio.windows([0,1440],[0,0],0)

Carabineros_phone_charger = Carabineros.Appliance(Carabineros,10,5,1,60,0.1,60)
Carabineros_phone_charger.windows([540,660],[0,0],0.1)

Carabineros_fridge = Carabineros.Appliance(Carabineros,2,250,1,1440,0,30,'yes',3)
Carabineros_fridge.windows([0,1440],[0,0])
Carabineros_fridge.specific_cycle_1(200,20,5,10)
Carabineros_fridge.specific_cycle_2(200,15,5,15)
Carabineros_fridge.specific_cycle_3(200,10,5,20)
Carabineros_fridge.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1440])

Carabineros_PC = Carabineros.Appliance(Carabineros,2,70,1,1440,0,1440, flat = 'yes')
Carabineros_PC.windows([0,1440],[0,0])

Carabineros_water_boiler = Carabineros.Appliance(Carabineros,2,1000,1,40,0.1,1)
Carabineros_water_boiler.windows([480,1080],[0,0],0.1)

Carabineros_printer = Carabineros.Appliance(Carabineros,2,25,1,15,0.1,1)
Carabineros_printer.windows([480,1080],[0,0],0.1)
