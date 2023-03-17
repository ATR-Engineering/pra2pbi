# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:43:02 2021

@author: BartRoseboom
"""

import requests
import json
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.io as pio
pio.renderers.default='browser'
#b.roseboom@p-r-a.nl:$gkmpOz$nF

login = 'Yi5yb3NlYm9vbUBwLXItYS5ubDo6JGdrbXBPeiRuRg=='
applicationID = '2LtcYHKHxlgs'

def Request(QSelect, SlugName, DateStart, DateEnd):
    i = 5000
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    while i == 5000:
        
        #QSelect = "QCC4"
        #SlugName = "mds-2-act-infeed-weight"
        
        # DateStart = "2022-2-8T08:00:00+00:00" #datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
        # DateEnd = "2022-2-9T12:00:00+00:00"
        
        ResponseList1 = ['Kraaijennest', 'QCC4', 'QCC1', 'QCC2', 'QCC3']
        Request1 = QSelect #ResponseList1[1]
        
        #Request2 = TagName #ResponseList2[13]
        
        ####################################################################################### 1 -> ontvangen API bearer token
        url = "https://api.ayayot.com:443/access-tokens?fields=secretId"
        payload = json.dumps({"expiresIn": 3600})
        headers = {
          'Api-Version': '2',
          'Api-Application': applicationID,
          'Content-Type': 'application/json',
          'Authorization': 'Basic '+login
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        
        my_headers = response.json()['data']
        token = my_headers['secretId']
        
        ####################################################################################### 2 -> selectie bedrijf
        url = "https://api.ayayot.com/companies?fields=publicId,name"
        
        payload={}
        headers = {
          'Api-Version': '2',
          'Content-Type': 'application/json',
        #  'Bearer': my_headers['secretId'],
          'Api-Application': applicationID,
          'Authorization': 'Bearer '+token
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)
        
        my_headers2 = response.json()['data'][0]
        companyId = my_headers2['publicId']
        
        ####################################################################################### 3 -> voor selectie device
        url = "https://api.ayayot.com/agents?fields=publicId,name,deviceId"
        
        payload={}
        headers = {
          'Api-Version': '2',
          'Api-Application': applicationID,
          'Api-Company': companyId,
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+token
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        print(response.text)
        
        my_headers3 = response.json()['data'][0]
        agentId = my_headers3['publicId']
        
        
        
        ####################################################################################### 4 -> Voor selectie Q
        url = "https://api.ayayot.com/agents/"+agentId+"/data-sources?fields=publicId,name,ipAddress"
        
        payload={}
        headers = {
          'Api-Version': '2',
          'Api-Application': applicationID,
          'Api-Company': companyId,
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+token
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        print(response.text)
        
        
        my_headers4 = response.json()['data']
        Q4_index = next((index for (index, d) in enumerate(my_headers4) if d['name'] == Request1), None)
        sourceId = response.json()['data'][Q4_index]['publicId'] # Q4
        # for i in range(0,4):
        #     print(response.json()['data'][i]['publicId'])
        
        ######################################################################################### 5a voor bepaling slug lijst niet compleet? max 19?
        # url = "https://portal.ixon.cloud:443/api/agents/2aOMc6x7cBeh/data-tags?fields=%2A"
        
        # headers = {
        #     "Accept": "application/json",
        #     "Api-Version": "2",
        #       'Api-Application': applicationID,
        #       'Api-Company': companyId,
        #       'Authorization': 'Bearer '+token
        # }
        
        # response = requests.request("GET", url, headers=headers)
        
        # print(response.text)
        
        # my_headers5 = response.json()['data']
        # #tagId =  response.json()['data'][13]['tagId']
        # #Q4_Tag = next((index for (index, d) in enumerate(my_headers5) if d['name'] == Request2), None)
        # #tagId = response.json()['data'][Q4_Tag]['slug']
        # #publicId = response.json()['data'][7]['publicId']
        
        ####################################################################################### 6 -> import data
        
        url = "https://api.ayayot.com/data"
        
    
        
        
        
        payload = """[\r\n
                       {\r\n
                        \"source\": {\r\n
                        \"publicId\": \""""+str(sourceId)+"""\"\r\n
                        },\r\n
                       \"tags\": [\r\n
                       {\r\n
                        \"preAggr\": \"raw\",\r\n
                        \"slug\": \""""+SlugName+"""\",\r\n
                        \"queries\": [\r\n
                            {\r\n
                                \"ref\": \"a\",\r\n
                                \"limit\": 5000,\r\n
                                \"offset\": 0\r\n
                                }\r\n
                            ]\r\n
                        }\r\n
                        ],\r\n
                        \"start\": \""""+DateStart+"""\",\r\n
                        \"end\": \""""+DateEnd+"""\",\r\n
                        \"timeZone\": \"Europe/Amsterdam\"\r\n
                        }\r\n
                        ]"""
        #                \"id\": \""""+str(tagId)+"""\",\r\n
        # act-infeed-weight
        # mds-2-act-infeed-weight
        # totalizer-weight-per-shift
        # mds-2-totalizer-weight-per-shift
        headers = {
          'Api-Version': '2',
          'Api-Application': applicationID,
          'Api-Company': companyId,
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+token
        }
        
        json_dump = json.dumps(payload)
        
        print(json_dump)
        
        json_object = json.loads(json_dump)
        
        response = requests.request("POST", url, headers=headers, data=json_object)
        
        print(response.text)
        
        my_headers6 = response.json()['data'][0]['points']
        
        
        df1 = pd.DataFrame.from_dict(my_headers6)
        df1['values'] = df1['values'].apply(pd.Series)
        i = len(df1)
        DateEnd = pd.to_datetime(str(df1.time.min())).strftime("%Y-%m-%dT%H:%M:%S+01:00")
        df2 = pd.concat([df1, df2], ignore_index=True)
    return df2

# df1['values2'] = df1['values']*60


##################################


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