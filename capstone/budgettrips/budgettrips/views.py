from django.shortcuts import render
import requests

def index(request):
    return render(request, 'index.html')

def search(request):
    return render(request, 'search.html')

def results(request):
    return render(request, 'results.html')

def login(request):
    return render(request, 'login.html')

def output(request):
    data=requests.get("https://reqres.in/api/users")
    print(data.text)
    data = data.text
    return render(request, 'home.html', {'data':data})

def parameters(request):
    origin = request.POST.get('origin', None)
    destination = request.POST.get('destination', None)
    depart = request.POST.get('depart', None)
    returnD = request.POST.get('return', None)
    adult = request.POST.get('adulttravelers', None)
    child = request.POST.get('childtravelers', None)
    budget = request.POST.get('budget', None)

    results = [origin, destination, depart, returnD, adult, child, budget]
    return render(request, 'results.html', {"Results":results})