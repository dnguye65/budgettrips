#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:30:02 2019

@author: duyennguyen
"""
import requests
import pandas as pd


origin = "CLT"
destination = "JFK"
departDate = "2019-12-01"
returnDate = "2019-12-05"

url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browseroutes/v1.0/US/USD/en-US/"+ origin+ "/"+ destination+ "/"+departDate + "/"+returnDate

querystring = {"inboundpartialdate":"2019-12-05"}

headers = {
      'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "5634543e8emsh51bbee6593a2705p1ae8c7jsnded43d3a44f0"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_data = response.json()


#create a 1D arraylist
my_list = []

#loop through each quotes to get the price 
for each in json_data['Quotes']:
    minprice = each['MinPrice']
    carrierid = each['OutboundLeg']['CarrierIds'].pop()
    #for each quotes, check to see if the carrierId match the carrierid in carrier list
    #grab the name based on the carrierId
    for i in json_data['Carriers']:
       if i['CarrierId'] == carrierid:
           airlineName = i['Name']
    #create a 2D array
    my_list.append([minprice, airlineName])


#convert 2D array to dataframe
df = pd.DataFrame(my_list, columns = ['Price', 'Airlines']) 
#sort based on the price
df1 = df.sort_values('Price', ascending=True)
#print it out
print(df1)







    