from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from textParser import parseFile
# from .forms import YourForm

# Create your views here.
def add_journal_request(request):
    return render(request, "templates/editingdatabase/adding.html")


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
#parse journal txt create num entries and journal entries and site etc
    with connection.cursor() as cursor:
        sql = "INSERT INTO journal (journalTitle, auth_fname,auth_lname, countryorigin, century) VALUES (%s, %s)"
        cursor.execute(sql, [journalTitle, auth_fname,auth_lname,countryorigin,century])
    return redirect('templates/editingdatabase/success.html')
    return render(request, 'adding.html', {'form': form})
