from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# from database_sisters.addJournal.forms import DocumentForm
from excel_reader import runExcelReader
from textParser import arrayMaker
# Create your views here.
def adding(request):
    if request.method == 'POST':
        context = {}
        journalTitle = request.POST.get('journalTitle')
        auth_fname = request.POST.get('auth_fname')
        auth_lname = request.POST.get('auth_lname')
        countryorigin = request.POST.get('countryorigin')
        countrytravel = request.POST.get('countrytravel')
        centuryOther = request.POST.get('other_box')
        centuryOtherNum = request.POST.get('otherNum')
        century18 = request.POST.get('18th')
        century19 = request.POST.get('19th')
        filetype = request.POST.get('filetype')
        file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(file.name, file)
        context['url'] = fs.url(name)

        centuryarr = []
        if centuryOther == "on":
            centuryarr.append(centuryOtherNum)
        if century18 == "on":
            centuryarr.append(18)
        if century19 == "on":
            centuryarr.append(19)
        #if file type is exel do
        journal_entry_data_array = []

        if filetype.endswith(".xlsx"):
            sites_column = request.POST.get('sites_column')
            city_column = request.POST.get('city_column')
            notes_column = request.POST.get('notes_column')
            sketch_column = request.POST.get('sketch_column')
            entry_column = request.POST.get('entry_column')
            date_column = request.POST.get('date_column')

            journal_entry_data_array = runExcelReader(file, date_column, entry_column, sites_column, sketch_column,
                                                      notes_column, city_column)
        elif filetype.endswith(".txt"):
            journal_entry_data_array = arrayMaker(file, centuryarr)
        else:
            return HttpResponse("incorrect file type")

        #else make excel file by parsing textparser

        num_entries = len(journal_entry_data_array)
        # return HttpResponse("File uploaded successfully")
            #make everything upper case
        #parse journal txt create num entries and journal entries and site etc
        # with connection.cursor() as cursor:
        #     # select exists(select * from table) returns 1 if exists
        #     # execute
        #     # result = cursor.fetchone()[0]
        #     # if result ==1 etc
        #     # DOES JOURNAL EXIST ALREADY
        #     sql = "INSERT INTO journal (journalTitle, num_entries, century) VALUES (%s, %s)"
        #     cursor.execute(sql, [journalTitle, num_entries, century])
        #     # author
        #     sql2 = "SELECT EXISTS(AUTH_FNAME, AUTH_LNAME FROM AUTHOR WHERE AUTH_FNAME = auth_fname AND AUTHLNAME = " \
        #            "auth_lname)"
        #     cursor.execute(sql2, [auth_fname, auth_lname])
        #     exists = cursor.fetchone()[0]
        # #     if exists == 0:  # DOESN'T EXIST
        # #         # CHECK IF COUNTRY ID EXISTS, ELSE MAKE NEW ONE
        # #         # make author, make author journal
        # #         sql3 = "INSERT INTO AUTHOR (AUTH_FNAME, AUTH_LNAME, COUNTRY_ID"
        # #     # MAKE AUTHOR-JOURNAL
        # #     sql4 = "INSERT INTO AUTHOR-JOURNAL(AUTH_ID, JOURNAL_ID) VALUES "
        #     country
        #     CHECK IF COUNTRY EXISTS, IF NOT MAKE ONE
        #     # journal country
        #     # MAKE JOURNAL-COUNTRY
        #
        #     JOURNAL ENTRIES
        #     ROW BY ROW,
        #     DATE
        #     SKETCH
        #     SITE
        #     INSERT JOURNAL ID, ENTRY TEXT, DATE FULL
        #     SITE_ENTRY
        #     DATE_ENTRY

            # return redirect('templates/addingJournal/success.html')


        return render(request, "adding.html", context)


#close cursor
#close connection
#but when?