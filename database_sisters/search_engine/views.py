from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def home(request):
    return render(request, "search_engine/home.html")

def results(request):

    if request.method == 'GET':
        table = request.GET["searchtype"]
        filters = request.GET.getlist("filter")
        filtermap = {}

        tables = ["journal", "journal_entry", "author", "sketch"]

        for filter in filters:
            filtermap[filter] = request.GET[filter]

        print(filtermap)

        if table not in tables:
            return render(request, "search_engine/results.html")    # illegal get request

        with connection.cursor() as cursor:

            query = "SELECT * FROM " + table

            cursor.execute(query)
            results = cursor.fetchall()

    return render(request, "search_engine/results.html", {"results": results})
