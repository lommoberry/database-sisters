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
            results, cols = journal_request(filter_map)
        
        elif table == "journal_entry":
            results, cols = journal_entry_request(filter_map)

        elif table =="author":
            results, cols = author_request(filter_map)

        elif table == "sketch":
            results, cols = sketch_request(filter_map)

        else:
            return render(request, "search_engine/results.html")    # illegal get request
        
    return render(request, "search_engine/results.html", {"results": results,  "cols": cols, "text": table=="journal_entry"})


def journal_request(filters):
    with connection.cursor() as cursor:

        cols = ["Title", "First", "Last", "Century", "Number of entries", "Country"]
        params = []

        query = """SELECT journal.journal_title, author.auth_fname, author.auth_lname, journal.century, journal.num_entries, country.country_name
                    FROM journal_country
                    LEFT JOIN country
                    ON journal_country.country_id = country.country_id
                    LEFT JOIN journal
                    ON journal_country.journal_id = journal.journal_id
                    LEFT JOIN author_journal
                    ON journal.journal_id=author_journal.journal_id
                    LEFT JOIN author
                    ON author.auth_id=author_journal.auth_id""" 
        
        if filters:
            query += " WHERE"

        for key, value in filters.items():
            query += " " + key + " LIKE %s AND"
            params.append(value)

        if query.endswith("AND"):
            query = query[:-3] + ";"

        cursor.execute(query, params)
        results = cursor.fetchall()

    return results, cols

def journal_entry_request(filters):
    with connection.cursor() as cursor:

        cols = ["Journal Title", "Century", "Site", "Country", "Date", "Text"]
        params = []

        query = """SELECT journal.journal_title, journal.century, site.site_name, country.country_name, date.date_full AS date, journal_entry.entry_text
                FROM site_entry   
                LEFT JOIN site
                ON site_entry.site_id = site.site_id
                LEFT JOIN journal_entry
                ON site_entry.entry_id = journal_entry.entry_id
                LEFT JOIN journal
                ON journal.journal_id=journal_entry.journal_id
                LEFT JOIN journal_country
                ON journal.journal_id=journal_country.journal_id
                LEFT JOIN country
                ON journal_country.country_id=country.country_id
                LEFT JOIN date_entry
                ON journal_entry.entry_id=date_entry.entry_id
                LEFT JOIN date
                ON date.date_full=date_entry.date_full
                """

        if filters:
            query += " WHERE"

        for key, value in filters.items():
            query += " " + key + " LIKE %s AND"
            params.append(value)

        if query.endswith("AND"):
            query = query[:-3]

        cursor.execute(query, params)
        results = cursor.fetchall()

    return results, cols
    
def author_request(filters):
    with connection.cursor() as cursor:

        params = []
        cols = ["First", "Last", "Country", "Journal"]

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

    return results, cols

# ?
def sketch_request(filters):
    with connection.cursor() as cursor:

        cols = ["sketch_id", "sketch"]

        query = "SELECT * FROM sketch"

        cursor.execute(query)
        results = cursor.fetchall()

    return results, cols

