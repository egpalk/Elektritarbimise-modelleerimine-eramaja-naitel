# -*- coding: utf-8 -*-
"""Daylight .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_c185jccuGeQ_hOukCt3qkL2tKQF5mF3
"""

import pandas as pd
import requests 
url = 'http://lennuki.myqnapcloud.com:8080/share.cgi?ssid=02mwhAw&fid=02mwhAw&filename=el.xlsx&openfolder=forcedownload&ep='

#get only dates
data_df = pd.read_excel(url,  header=1)
data_df = data_df.iloc[12456:82584] #from 2013 we have hourly data, drop rows before that. Drop values of year 2021
data_df.drop(data_df.columns[[2,3]],axis=1,inplace=True) 

date_info_df = data_df["Tund"].str.split(" ", expand = True)
data_df['Date']= date_info_df[0] 
data_df['Date']=pd.to_datetime(data_df['Date'], format='%d.%m.%Y')

data_df.drop(data_df.columns[[0,1]],axis=1,inplace=True)

data_df.drop_duplicates(inplace=True)
data_df.reset_index(inplace=True, drop=True)

data_df["day_length"] = ""

api = "https://api.sunrise-sunset.org/json?lat=59.385099744474196&lng=24.689724180918640&date="
for i in range(len(data_df)) : 
  date = data_df.loc[i, "Date"].strftime("%Y-%m-%d")
  api_request = api + date
  r = requests.get(url = api_request)
  data = r.json() 
  day_length = data['results']['day_length']
  length_list = day_length.split(':')
  minutes = int(length_list[0])*60 + int(length_list[1])
  data_df.loc[i, "day_length"] = minutes

#write to csv
#Saved to here http://lennuki.myqnapcloud.com:8080/share.cgi?ssid=0j0PWw1&fid=0j0PWw1&filename=day_length.csv&openfolder=forcedownload&ep=