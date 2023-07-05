from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, "search_engine/home.html")

def results(request):

    if request.method == 'GET':
        searchType = request.GET["searchtype"]
        filters = request.GET.getlist("filter")

        print(searchType)

        for entry in filters:
            print(entry + " " + request.GET[entry])

    return render(request, "search_engine/results.html")
