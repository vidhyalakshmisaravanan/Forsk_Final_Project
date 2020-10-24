# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 17:16:51 2020

@author: ELCOT
"""

import pandas as pd
import numpy as np
import re
import datetime

def datetime_divider(data):   #20190623 034523
    
    for index in range (len(data)):
        if (re.match("^\d",str(data[index]))):
            regex = re.compile("\d{1,8}")
            a = regex.findall(str(data[index]))
            
            data[index ] = [ a[0] , a[1] ]
        else:
            data[index ] = [np.nan, np.nan]
    return data



    

def call_time_fetcher(data):
    for index in range(len(data)):
        data[index] = str(data[index])
        if data[index]!="nan":
            year = data[index][:4]
            month = data[index][4:6]
            day = data[index][6:8]
            hours = data[index][8:10] 
            minutes = data[index][10:12]
            seconds = str(round(float(data[index][12:])))
            if int(seconds) >= 60:
                seconds = int(seconds) -60
                minutes = int(minutes)+1 
            if int(minutes) >=60:
                hours = int(hours)+1
                minutes  = int(minutes) - 60 
            data[index] = f"{year}-{month}-{day} {hours}:{minutes}:{seconds}"
        else:
            data[index] = np.nan
    return data
    
def time_modifier(data):  #032717   03.27.17am
    for i in range(len(data)):
        data[i]=str(data[i])
        
        if re.match("^\d",(data[i])):
            m=int(data[i][:2])
            mn=data[i][2:4] 
            
            sec=data[i][4:]
            
            if m >=12:
                if m==12:
                    hr=str(m)
                else:
                    hr=str(m-12)
                merd="pm"
            else:
                if m==0:
                    hr=str(12)
                else:
                    hr=data[i][:2]
                merd="am"    
                 
            
            
            data[i]=".".join([hr,mn,sec])+""+merd
            
            
        else:
            data[i]=np.nan
           
    return data
           
    
    
def date_modifier(data):
    # data type of data is list
    # 20190620 should be converted to 2019-06-20
    for index in range(len(data)):
        if re.match("^\d", str(data[index])):
            year = str(data[index][:4])
            month = str(data[index][4:6])
            day = str(data[index][6:])
            data[index] = "-".join([year, month, day])
        else:
            data[index] =  np.nan
            
    return data


def hourly_range(data): 
        for index in range(len(data)):
            data[index]=str(data[index])
            if data[index]!="nan":
                if re.search("pm",data[index]):
                   time_data=re.findall("\d",data[index])
                   if int(time_data[0])!="12":
                      time_data=int(time_data[0])+12
                   else:  
                      time_data=time_data[0]
                else:
                      time_data=re.findall("\d",data[index])
                      if int(time_data[0])==12:
                        time_data=f"0 {int(time_data[0])-12}"
                      else:  
                        time_data=time_data[0]
                data[index]=f"{time_data}:00-{time_data}:59"
                
            else:
                data[index]="np.nan"
        return data        


def replace_simple_termi(data):
        data[5]= data[5].replace("Originating","Outgoing")
        data[5]= data[5].replace("Terminating","Incomming")
        data[267]=data[267].replace("Success","Voice Portal")
        data[312]=data[312]. replace("Shared Call Appearance","Secondary Device")
        return data    
    
    
def remove_unwanted_data(data):
        for index in range(len(data)):
            if data[index]=="Secondary Device" or data[index]=="Primary Device":
                continue
            else:
                data[index]=np.nan
        return data      


def weekly_range(data):
         for index in range(len(data)):
             data[index]=str(data[index])
             if data[index]!="nan":
                 year,month,day=[int(x) for x in data[index].split("-")]
                 result=datetime.date(year,month,day)
                 data[index]=result.strftime("%A")
         else:
             data[index]=np.nan
         return data      
 



def combine_All_Services(data1, data2, data3):
    for index in range(len(data1)):
        if data1[index] is np.nan:
            
            if data2[index] is not np.nan and data3[index] is not np.nan:
                data1[index] = str(data2[index])+ "," + str(data3[index])
            
            elif data2[index] is not np.nan:
                data1[index] = data2[index]
            
            else:
                data1[index] = data3[index]
            
        else:
            continue
    return data1


dataset_name="raw_dat81.csv"
df = pd.read_csv(dataset_name,header=None,low_memory=False)

df["date"],df["time"]  = zip(*datetime_divider(df[9].tolist()))

print(df["date"].head())
print(df["time"].head())

df["time"]=time_modifier(df["time"])
print(df["time"].head())



df["hourly_range"]=hourly_range(df["time"])
print(df["hourly_range"])

print(df["date"] )
df["date"] = date_modifier( df["date"].tolist() )
print(df["date"])

df["weekly_range"]= weekly_range(df["date"].tolist())
print(df["weekly_range"].tolist())  


print (df[13])
df["endtime"] = pd.to_datetime(call_time_fetcher(df[13].tolist()))
print(df["endtime"])


print (df[9])
df["starttime"] = pd.to_datetime(call_time_fetcher(df[9].tolist()))
print(df["starttime"])

 
df["duration"] =(df["endtime"]-df["starttime"]).astype("timedelta64[m]")
print(df["duration"])



    
print(df[5].unique())
print(df[267].unique())
print(df[312].unique())

df=replace_simple_termi(df)

print(df[5].unique())
print(df[267].unique())
print(df[312].unique())




print(df[312].unique())
df[312]=remove_unwanted_data(df[312])
print(df[312].tolist())






data1=["Primary Device","Simultaneous Ring Personal","Secomdary Device","Remote Office","simultaneous Ring Personal"]
data2=["Primary Device","Secondary Device","Primary Device","Secondary Device","Primary Device"]  
data3=["Voice Portal"]
result=combine_All_Services(data1,data2,data3)
print(result)






df = df.drop("time", axis=1) 
df.to_csv("new_cdr_data.csv", index = None)