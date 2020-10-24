# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 06:21:42 2020

@author: ELCOT
"""

import pandas as pd


def main():
    
    dataset_name =  "new_cdr_data.csv"
    
    call_columns = ["4", "5","14", "31", "120", "147", "267", "312", "345", 
                    "date","starttime", "endtime","duration","hourly_range","weekly_range"]
        
    call_dataset = pd.read_csv(dataset_name, usecols = call_columns,low_memory = False)

    service_columns = ["31", "120", "147", "345","date", "starttime", "endtime","duration"]
    
    service_dataset = call_dataset[service_columns]
    
    
    
    device_columns = ["5", "31", "120", "312", "345", "date","starttime", "endtime","duration"]
    device_dataset = call_dataset[device_columns]
    
    
    call_dataset = call_dataset.rename(columns = {"4":"Group", "5":"Call_Direction","14":"Missed Calls",
                                            "31":"GroupID", "120":"UserID", "147":"Features", "267":" vpDialingfacResult",
                                            "312":"UsageDeviceType",
                                            "345":"UserDeviceType"})
    
    
    
    service_dataset = service_dataset.rename(columns={"120":"UserID", 
                                                  "31":"GroupID", "147":"FeatureName",
                                                  "345":"UserDeviceType","date":"FeatureEventDate" })


    device_dataset = device_dataset.rename(columns={"5": "DeviceEventTypeDirection", 
     
                                                    "120":"UserID", "31":"GroupID", "345":"UserDeviceType","date":"DeviceEventDate","312":"UsageDeviceType"})
    call_dataset.to_csv("Call_data.csv", index=None)
    service_dataset.to_csv("Service_data.csv", index=None)
    device_dataset.to_csv("Device_data.csv", index=None)
    
    

if(__name__=="__main__"):
    main()
