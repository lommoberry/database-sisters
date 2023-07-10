from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from textParser import parseFile
# from .forms import YourForm

# Create your views here.
def add_journal_request(request):
    return render(request, "templates/editingdatabase/adding.html")

def entry_parser():
    #make entry, site, site entry, sketch, date, date_entry
    pass

def add_data(request):
    if request.method == 'POST':
    #     form = YourForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('success')  # Redirect to a success page
    # else:
    #     form = YourForm()
        journalTitle = request.POST.get('journalTitle')
        auth_fname = request.POST.get('auth_fname')
        auth_lname = request.POST.get('auth_lname')
        countryorigin = request.POST.get('countryorigin')
        countrytravel = request.POST.get('countrytravel')
        century = request.POST.get('century')
        file = request.POST.get('file')
    # print("did something")

    #make everything upper case
#parse journal txt create num entries and journal entries and site etc
    with connection.cursor() as cursor:
        #select exists(select * from table) returns 1 if exists
        #execute
        #result = cursor.fetchone()[0]
        #if result ==1 etc
        sql = "INSERT INTO journal (journalTitle, num_entries, century) VALUES (%s, %s)"
        cursor.execute(sql, [journalTitle, num_entries,century])
        #author
        #country
        #journal country
        sql = "INSERT INTO author-journal ("

    return redirect('templates/editingdatabase/success.html')
    return render(request, 'adding.html', {'form': form})


#close cursor
#close connection
#but when?