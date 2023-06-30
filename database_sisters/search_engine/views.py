from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "search_engine/home.html")

def results(request):

    if request.method == 'GET':
        searchQuery = request.GET["search"]
        filters = request.GET.getlist("filter")

        print(searchQuery)

    return render(request, "search_engine/results.html")
