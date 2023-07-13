from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
# from excel_reader import runExcelReader
# from .forms import YourForm

# Create your views here.
def add_journal_request(request):
    return render(request, "editingdatabase/add_journal.html")

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

    #if file type is exel do
    #else make excel file by parsing textparser

    file_path = "C:/Users/bridg/PycharmProjects/database-sisters/database_sisters/justPlayin/3.xlsx"
    journal_entry_data_array = runExcelReader(file_path, 0, 1, 2, 3, 4, 5)
    num_entries = len(journal_entry_data_array)
    #make everything upper case
#parse journal txt create num entries and journal entries and site etc
    with connection.cursor() as cursor:
        #select exists(select * from table) returns 1 if exists
        #execute
        #result = cursor.fetchone()[0]
        #if result ==1 etc
        #DOES JOURNAL EXIST ALREADY
        sql = "INSERT INTO journal (journalTitle, num_entries, century) VALUES (%s, %s)"
        cursor.execute(sql, [journalTitle, num_entries, century])
        #author
        sql2 = "SELECT EXISTS(AUTH_FNAME, AUTH_LNAME FROM AUTHOR WHERE AUTH_FNAME = auth_fname AND AUTHLNAME = " \
               "auth_lname)"
        cursor.execute(sql2, [auth_fname, auth_lname])
        exists = cursor.fetchone()[0]
        if exists == 0:#DOESN'T EXIST
            #CHECK IF COUNTRY ID EXISTS, ELSE MAKE NEW ONE
            #make author, make author journal
            sql3 = "INSERT INTO AUTHOR (AUTH_FNAME, AUTH_LNAME, COUNTRY_ID"
        #MAKE AUTHOR-JOURNAL
        sql4 = "INSERT INTO AUTHOR-JOURNAL(AUTH_ID, JOURNAL_ID) VALUES "
        #country
        #CHECK IF COUNTRY EXISTS, IF NOT MAKE ONE
        #journal country
        #MAKE JOURNAL-COUNTRY

        #JOURNAL ENTRIES
        #ROW BY ROW,
        # DATE
        # SKETCH
        # SITE
        # INSERT JOURNAL ID, ENTRY TEXT, DATE FULL
        #SITE_ENTRY
        #DATE_ENTRY

    return redirect('templates/editingdatabase/success.html')
    return render(request, 'adding.html', {'form': form})


#close cursor
#close connection
#but when?