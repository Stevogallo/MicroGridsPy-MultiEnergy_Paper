# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 17:12:44 2019

@author: stevo
"""

import pandas as pd

PV = pd.read_excel('PV_Output.xlsx')
SC = pd.read_excel('SolarCollector_Output.xlsx')

PV.to_csv('PV_Output.csv')
SC.to_csv('SC_Output.csv')