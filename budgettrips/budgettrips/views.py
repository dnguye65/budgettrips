from django.shortcuts import render
import requests
import pandas as pd

def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

def results(request):
    return render(request, 'results.html')

def login(request):
    return render(request, 'login.html')

def parameters(request):
    origin = request.POST.get('origin')
    destination = request.POST.get('destination')
    str_budget = request.POST.get('budget')
    departDate = request.POST.get('depart')
    returnDate = request.POST.get('return')

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
    df = df.head(5)
    #sort based on the price
    df = df.sort_values('Price', ascending=True)
    #result = df.values.tolist()
        
    #if empty string, print the result as is
    if not str_budget.strip():
        result = df.values.tolist()
    else:
        df3 = df[~(df['Price'] >= float(str_budget))]  
        result = df3.values.tolist()
    return render(request, 'results.html', {"result":result})