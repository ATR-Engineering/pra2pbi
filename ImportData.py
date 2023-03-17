# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 13:42:04 2023

@author: ATR Engineering1
"""

import pandas as pd
import os
import plotly.express as px
import plotly.io as pio
import datetime as dt
import time
import calendar
import numpy as np
import seaborn as sns
import plotly.graph_objs as go
from datetime import date, datetime, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import sys
from matplotlib.ticker import PercentFormatter
#pio.renderers.default = 'browser'
import webbrowser
import requests
import json
pio.renderers.default='browser'
#b.roseboom@p-r-a.nl:$gkmpOz$nF

login = 'Yi5yb3NlYm9vbUBwLXItYS5ubDo6JGdrbXBPeiRuRg=='
applicationID = '2LtcYHKHxlgs'
EfficiencyTarget = 2500 # 2x 1250
minDate = date(2021, 1, 27) # after this date the time was started being registered on the Q file
dfOEE1TimeDelta = 60 # time in days, standaard 60
WeekdaysOffset = 0 # change timeframe from monday to wednesday
MinWeight = 170 # minimum weight to count as downtime
MaxWeight = 11000 # filter for dosco mistakes
#for file in folder

"""
from PRAImportData import LabDAMDS
result = LabDAMDS() 
dfQ2 = result[0]
dfQMDS2 = result[1]
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:43:02 2021

@author: BartRoseboom
"""


from IxonAPI2 import Request


def DowntimeCalculator(key,value, DateStart, DateEnd):
    #ImportName = "act-infeed-weight"
    df20 = Request("QCC0", value, DateStart, DateEnd)
    ColumnName = key+"Downtime"
    ColumnName2 = key+"PlannedTime"
    ColumnName3 = key+"RunningTime"
    df20.time = pd.to_datetime(df20.time, errors='coerce', utc=True)
    
    df20[ColumnName] = np.where(df20['values'] < MinWeight, 15, 0)
    
    df20 = df20.drop_duplicates()
    df20 = df20.sort_values(by=['time'])
    df20['time'] = df20.time.dt.ceil('15min') 
    df20a = pd.date_range(start= df20.time.min().floor(freq='15min'), end= df20.time.max().ceil(freq='15min'), freq='15min' )
    df20 = df20.set_index('time')
    df20=df20.reindex(df20a, fill_value=0)    
    
    df20[ColumnName2] = 15
    df20[ColumnName3] = df20[ColumnName2] - df20[ColumnName]
    df20.rename(columns = {'values': value}, inplace = True)

    return df20

DateStart = (dt.datetime.now() - dt.timedelta(hours = (24*dfOEE1TimeDelta))).strftime("%Y-%m-%dT%H:%M:%S+01:00") #"2022-2-8T08:00:00+00:00" #dt.datetime.now().strftime("%Y-%m-%d-%H%M")
DateEnd = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00") #"2022-2-9T12:00:00+00:00"
ImportGroups = {"MDS1":"mds-1-act-infeed-weight", "MDS2":"mds-2-act-infeed-weight"}
#ImportGroups = {"MDS1":"act-weight-per-shift", "MDS2":"mds-2-totalizer-weight-per-shift"}

df20 = DowntimeCalculator("MDS1", ImportGroups["MDS1"], DateStart, DateEnd)
df20.loc[df20["mds-1-act-infeed-weight"] > 3000, "mds-1-act-infeed-weight"] = 0
#df20 = df20.drop(df20[df20["act-infeed-weight"] > 3400].index)
#df20['act-infeed-weight'] = df20['act-infeed-weight'] / 12
df30 = DowntimeCalculator("MDS2", ImportGroups["MDS2"], DateStart, DateEnd)
#df30['mds-2-act-infeed-weight'] = df30['mds-2-act-infeed-weight'] / 12
df32 = pd.merge(df20, df30, left_index=True, right_index=True)

df32 = df32.rename_axis('time').reset_index()

dfOEE1TimeDelta = 60 # time in days, standaard 60
df40 = Request("QCC0","mds-1-act-infeed-weight", DateStart, DateEnd)
df39 = Request("QCC0","mds-2-act-infeed-weight", DateStart, DateEnd)