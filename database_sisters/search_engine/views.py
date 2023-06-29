from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "search_engine/home.html")

def results(request, query):
    return render(request, "search_engine/results.html")
