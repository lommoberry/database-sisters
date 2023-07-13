from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection

def home(request):
    return render(request, "search_engine/home.html")

def results(request):

    if request.method == 'GET':
        table = request.GET["searchtype"]
        filters = request.GET.getlist("filter")
        filter_map = {}

        for filter in filters:
            filter_map[filter] = request.GET[filter]

        if table == "journal":
            results = journal_request(filter_map)
        
        elif table == "journal_entry":
            results = journal_entry_request(filter_map)

        elif table =="author":
            results = author_request(filter_map)

        elif table == "sketch":
            results = sketch_request(filter_map)

        else:
            return render(request, "search_engine/results.html")    # illegal get request
        
    return render(request, "search_engine/results.html", {"results": results})


def journal_request(filters):
    with connection.cursor() as cursor:

        query = "SELECT * FROM journal" 

        cursor.execute(query)
        results = cursor.fetchall()

    return results

def journal_entry_request(filters):
    with connection.cursor() as cursor:

        query = "SELECT * FROM journal_entry"

        cursor.execute(query)
        results = cursor.fetchall()

    return results
    
def author_request(filters):
    with connection.cursor() as cursor:

        params = []

        query = """SELECT author.auth_fname, author.auth_lname, country.country_name, journal.journal_title
                    FROM author_journal 
                    LEFT JOIN author 
                    ON author_journal.auth_id = author.auth_id
                    LEFT JOIN journal
                    ON author_journal.journal_id = journal.journal_id
                    LEFT JOIN country
                    ON country.country_id = author.country_id"""
        
        if filters:
            query += " WHERE"

        for key, value in filters.items():
            query += " " + key + " LIKE %s AND"
            params.append(value)

        if query.endswith("AND"):
            query = query[:-3]

        cursor.execute(query, params)
        results = cursor.fetchall()

    return results

def sketch_request(filters):
    with connection.cursor() as cursor:

        query = "SELECT * FROM sketch"

        cursor.execute(query)
        results = cursor.fetchall()

    return results

