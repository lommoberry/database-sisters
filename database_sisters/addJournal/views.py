from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# from database_sisters.addJournal.forms import DocumentForm
# Bridget Kim xpt3bn
import re
import openpyxl
import string

# check file type, if xlsx give option to select column numbers
# if txt, say its not guaranteed to be correct but it will try
# will only do journals so has to have dates

def parse_excel_file(file, column_indexes=None):
    wb = openpyxl.load_workbook(file)  # Load the Excel file
    sheet = wb.active  # Select the active sheet (or specify a specific sheet name)

    data = []  # List to store the parsed data
    # journal date, location = sites, notes, sites, sketch,  country=italy

    for row in sheet.iter_rows(values_only=True):
        if column_indexes:
            selected_columns = [row[i] for i in column_indexes]
            if (selected_columns[0] == None):
                break
            data.append(selected_columns)
        else:
            roww = list(row)
            if (roww[1] == None):
                break
            data.append(roww)

    return data

def runExcelReader(file, date, entry, locations, sketch, note, city):
# filepath = "C:/Users/bridg/Downloads/Italian_Journey_Rome_Naples_clean.txt"
# filepath = "C:/Users/bridg/Downloads/ItalianJourney1786-1788onlyentries(1).txt"
# parse_text_file(filepath)
# date, entry, locations, sketch, note, city
    column_indexes = [int(date), int(entry), int(locations), int(sketch), int(note), int(city)]
    parsed_data = parse_excel_file(file, column_indexes)

# Separate arrays for each row
    rows = parsed_data
    return rows
# if no day, then check before entry and after entry and make it equal to that
# check every paragraph's first line for a date
# Bridget Kim xpt3bn
# file_path = "/database_sisters/justPlayin/3.xlsx"
# runExcelReader(file_path, 0, 1, 2, 3, 4, 5)
# Bridget Kim xpt3bn
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
import re
import datefinder
from dateutil import parser
from datetime import datetime
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


#check file type, if xlsx give option to select column numbers
#if txt, say its not guaranteed to be correct but it will try
#will only do journals so has to have dates

def entry_parser_findNotes(entry):
    note_pattern = r"note:\s(.*)"
    note_matches = re.findall(note_pattern, entry)
    sidenote_content = ""
    for match in note_matches:
        sidenote_content += match.strip() + ", "

    return sidenote_content.upper()


def entry_parser_findCity(entry):
    words = nltk.word_tokenize(entry)
    tagged_words = nltk.pos_tag(words)
    entities = nltk.chunk.ne_chunk(tagged_words)
    # ORG = organization, PER = person, GPE=Geo politicla entity, LOC=location, DATE, TIME, MONEY, PERCENT, FACILITY
    locations = []
    string = ""
    for entity in entities:
        if hasattr(entity, 'label') and (entity.label() == 'GPE'):
            locations.append(', '.join(word for word, tag in entity.leaves()))
    for i in range(len(locations)):
        string += locations[i].upper() + ", "
    return string


def entry_parser_findSites(entry):
    words = nltk.word_tokenize(entry)
    tagged_words = nltk.pos_tag(words)
    entities = nltk.chunk.ne_chunk(tagged_words)
#ORG = organization, PER = person, GPE=Geo politicla entity, LOC=location, DATE, TIME, MONEY, PERCENT, FACILITY
    locations = []
    string = ""
    for entity in entities:
        if hasattr(entity, 'label') and (entity.label() == 'FACILITY' or entity.label() == 'LOC'):
            locations.append(', '.join(word for word, tag in entity.leaves()))
    for i in range(len(locations)):
        string += locations[i].upper() + ", "
    return string

# def raw_date_cleaner(entry):
#     date_raw = entry.split('\n')[0]
#     words = word_tokenize(date_raw)
#     tagged_words = pos_tag(words)
#     date = ''
#     for i in range(len(tagged_words)):
#         if tagged_words[i][1] == 'CD':
#             date = tagged_words[i][0]
#             break
#     if date:
#         # print(date)
#         date_str = date.strip()  # Remove newline character
#         # Parse the input date string using datetime
#         parsed_date = datetime.strptime(date_str, "%B, %Y-%m-%d")
#         # Format the date as MM-DD-YYYY
#         formatted_date = parsed_date.strftime("%m-%d-%Y")
#         return formatted_date
#     else:
#         return None



def arrayMaker(file, century):
    entry_array =[]
    dates = []
    text = ""
    # with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            match = parser.parse(line, fuzzy_with_tokens=True)
            if match:
                for i in century:
                    year = str(i - 1)
                    date = str(match[0].date())
                    if date.startswith(year):
                        entry_array.append(text.strip())
                        text = ""
                        dates.append(date)
                        pass

        except:
            text += str(line)
    file.close()

    entry_array.pop(0)
    num_rows = len(entry_array)

    array = [[''] * 6 for _ in range(num_rows)]
    #add in things
    for row in range(num_rows):
        entry = entry_array[row]
        for col in range(6):
            if col==0:
                #date
                # print(row,col)
                array[row][col] = dates[row]
                pass
            elif col==1:
                #entry
                # print(row, col)
                array[row][col] = entry
                pass
            elif col==2:
                #locations
                # print(row, col)
                array[row][col] = entry_parser_findSites(entry)
                pass
            elif col==3:
                #sketches
                # print(row, col)
                array[row][col] = None
                pass
            elif col==4:
                #notes
                # print(row, col)
                array[row][col] = entry_parser_findNotes(entry)
                pass
            elif col==5:
                #city
                # print(row, col)
                array[row][col] = entry_parser_findCity(entry)
                pass
            else:
                pass
    return array



# Create your views here.
def adding(request):
    context = {}
    if request.method == 'POST':
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
        # print("requested file")
        fs = FileSystemStorage()
        # print("did fs")
        name = fs.save(str(file.name), file)
        # print("did name")
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

        if file.name.endswith(".xlsx"):
            sites_column = request.POST.get('sites_column')
            city_column = request.POST.get('city_column')
            notes_column = request.POST.get('notes_column')
            sketch_column = request.POST.get('sketch_column')
            entry_column = request.POST.get('entry_column')
            date_column = request.POST.get('date_column')

            journal_entry_data_array = runExcelReader(file, date_column, entry_column, sites_column, sketch_column,
                                                      notes_column, city_column)
        elif file.name.endswith(".txt"):
            journal_entry_data_array = arrayMaker(file, centuryarr)
        else:
            return HttpResponse("incorrect file type")

        #else make excel file by parsing textparser

        num_entries = len(journal_entry_data_array)

        with connection.cursor() as cursor:
            
            cursor.execute("""INSERT OR IGNORE INTO country (country_name) VALUES(%s)""", [countryorigin])
            cursor.execute("""INSERT OR IGNORE INTO country (country_name) VALUES(%s)""", [countrytravel])


            cursor.execute("""SELECT country_id FROM country WHERE country_name LIKE %s""", [countryorigin])

            origincountryID = cursor.fetchone()
            origincountryID = int(origincountryID[0])

            cursor.execute("""SELECT country_id FROM country WHERE country_name LIKE %s""", [countrytravel])
            countrytravelID = cursor.fetchone()
            countrytravelID = int(countrytravelID[0])

            authorSQL = """
                        INSERT OR IGNORE INTO author (auth_fname, auth_lname, country_id) 
                        VALUES(%s, %s, %s)
                        """

            cursor.execute(authorSQL, [auth_fname, auth_lname, origincountryID])

            cursor.execute("""SELECT auth_id FROM author WHERE auth_fname=%s AND auth_lname=%s""", [auth_fname, auth_lname])
            authorID = cursor.fetchone()
            authorID = int(authorID[0])

            journalSQL = """
                        INSERT OR IGNORE into journal (num_entries, century, journal_title)
                        VALUES(%s, %s, %s)
                        """
            
            cursor.execute(journalSQL, [num_entries, centuryarr[0], journalTitle])

            cursor.execute("""SELECT journal_id FROM journal WHERE journal_title=%s""", [journalTitle])
            journalID = cursor.fetchone()
            journalID = int(journalID[0])

            cursor.execute("""INSERT OR IGNORE into author_journal VALUES(%s, %s)""", [authorID, journalID])
            cursor.execute("""INSERT OR IGNORE into journal_country VALUES(%s, %s)""", [countrytravelID, journalID])

            # date, entry, locations, sketch, note, city
            for entry in journal_entry_data_array:
                cursor.execute("""INSERT OR IGNORE INTO date VALUES (%s)""", [entry[0]])

                
                if entry[5]:
                    cursor.execute("""INSERT OR IGNORE INTO site (site_name, country_id) VALUES(%s, %s)""", [string.capwords(entry[5]), countrytravelID])
                    cursor.execute("""SELECT site_id FROM site where site_name=%s""", [string.capwords(entry[5])])
                    site_id = cursor.fetchone()
                    site_id = int(site_id[0])

                else:
                    cursor.execute("""INSERT OR IGNORE INTO site (site_name, country_id) VALUES(%s, %s)""", ["Unknown", countrytravelID])
                    cursor.execute("""SELECT site_id FROM site where site_name=%s""", ["Unknown"])
                    site_id = cursor.fetchone()
                    site_id = int(site_id[0])

                

                if entry[3]:
                    cursor.execute("""INSERT OR IGNORE INTO sketch (sketch) VALUES(%s)""", [entry[3]])
                    cursor.execute("""SELECT sketch_id FROM sketch WHERE sketch=%s""", [entry[3]])

                    sketch_id = cursor.fetchone()
                    sketch_id = int(sketch_id[0])

                if sketch_id:
                    cursor.execute("""INSERT OR IGNORE INTO journal_entry (journal_id, entry_text, sketch_id) VALUES(%s, %s, %s)""", [journalID, entry[1].replace("_","").strip(), sketch_id])
                    cursor.execute("""SELECT entry_id FROM journal_entry WHERE entry_text=%s""", [entry[1].replace("_","").strip()])
                    entry_id = cursor.fetchone()
                    entry_id = int(entry_id[0])

                else: 
                    cursor.execute("""INSERT OR IGNORE INTO journal_entry (journal_id, entry_text) VALUES(%s, %s)""", [journalID, entry[1].replace("_","").strip()])
                    cursor.execute("""SELECT entry_id FROM journal_entry WHERE entry_text=%s""", [entry[1].replace("_","").strip()])
                    entry_id = cursor.fetchone()
                    entry_id = int(entry_id[0])

                cursor.execute("""INSERT OR IGNORE INTO date_entry VALUES(%s, %s)""", [entry_id, entry[0]])
                cursor.execute("""INSERT OR IGNORE INTO site_entry VALUES(%s, %s)""", [site_id, entry_id])
                    


        # return HttpResponse("File uploaded successfully")
            #make everything upper case
        #parse journal txt create num entries and journal entries and site etc
        # with connection.cursor() as cursor:
        #     sql1 = "select exists(select * where journalTitle == journalTitle)"
        #     # execute
        #     result = cursor.fetchone()[0]
        #     if result ==1:
        #         #journal exists
        #         return HttpResponse("Journal already exists")
        #     # DOES JOURNAL EXIST ALREADY
        #     sql = "INSERT INTO journal (journalTitle, num_entries, century) VALUES (%s, %s)"
        #     cursor.execute(sql, [journalTitle, num_entries, centuryarr])
        #     # author
        #     sql2 = "SELECT EXISTS(SELECT AUTH_FNAME, AUTH_LNAME FROM AUTHOR WHERE AUTH_FNAME = auth_fname AND " \
        #            "AUTHLNAME = " \
        #            "auth_lname)"
        #     cursor.execute(sql2, [auth_fname, auth_lname])
        #     exists = cursor.fetchone()[0]
        #     if exists == 0:  # DOESN'T EXIST
        #         sql3 = "SELECT EXISTS(SELECT COUNTRYID WHERE Countryname = country)"
        #         cursor.execute(sql3, [countryorigin])
        #         exists = cursor.fetchone()[0]
        #         if exists == 0:
        # #         # CHECK IF COUNTRY ID EXISTS, ELSE MAKE NEW ONE
        #             sql4 = "INSERT INTO COUNTRY(COUNTRYNAME) VALUES = (%s)"
        #             cursor.execute(sql4, countryorigin)
        # #         # make author, make author journal
        #             SELECT countryid
        #             sql5 = "INSERT INTO AUTHOR (AUTH_FNAME, AUTH_LNAME, COUNTRY_ID"
        #     # MAKE AUTHOR-JOURNAL
        #     sql4 = "INSERT INTO AUTHOR-JOURNAL(AUTH_ID, JOURNAL_ID) VALUES "
        #     country
        #     CHECK IF COUNTRY EXISTS, IF NOT MAKE ONE
            # journal country
            # MAKE JOURNAL-COUNTRY

            # JOURNAL ENTRIES
            # ROW BY ROW,
            # DATE
            # SKETCH
            # SITE
            # INSERT JOURNAL ID, ENTRY TEXT, DATE FULL
            # SITE_ENTRY
            # DATE_ENTRY

            # return redirect('templates/addJournal/success.html')


    return render(request, "adding.html", context)
    # return render(request, "success.html")

def editing(request):
    titleOrfirstname=request.GET.get('titleOrfirstname')
    firstOrlastname=request.GET.get('firstOrlastname')
    centuryOrJournal=request.GET.get('centuryOrJournal')

    date=request.GET.get('date')
    text=request.GET.get('text')
    titleJournal=request.GET.get('title')
    if date==None :
        if centuryOrJournal.isdigit():
            #is journal
            objj=titleOrfirstname #is title in this case
            # if request.method == 'POST':
            #     # newdate = request.POST.get('newdate')
            #     newtext = request.POST.get('newentry')
            #     with connection.cursor() as cursor:
            #         # try:
            #         query = "SELECT JOURNAL_ID FROM JOURNAL WHERE JOURNAL_TITLE = %s"
            #         var = [titleJournal]
            #         cursor.execute(query, var)
            #         journalID = cursor.fetchone()[0]
            #         sql = "UPDATE JOURNAL_ENTRY SET ENTRY_TEXT = %s WHERE JOURNAL_ID = %s AND ENTRY_TEXT " \
            #               "like %s"
            #         variables = [newtext, journalID, text]
            #         cursor.execute(sql, variables)
            #         # sss = "SELECT ENTRY_ID FROM JOURNAL_ENTRY WHERE ENTRY_TEXT like %s"
            #         # v = [newtext]
            #         # cursor.execute(sss, v)
            #         # entryID = cursor.fetchone()[0]
            #         # s = "UPDATE DATE_ENTRY SET DATE_FULL = %s WHERE ENTRY_ID = %s AND DATE_FULL = %s"
            #         cursor.connection.commit()
            #         # cursor.execute(s,[newdate,entryID,date])
            #         return HttpResponse("edited successfully")
                # except:
        else:
            #is author
            objj=titleOrfirstname + ", "+firstOrlastname#is first, lastname in this case
            # if request.method == 'POST':
            #     # newdate = request.POST.get('newdate')
            #     newtext = request.POST.get('newentry')
            #     with connection.cursor() as cursor:
            #         # try:
            #         query = "SELECT JOURNAL_ID FROM JOURNAL WHERE JOURNAL_TITLE = %s"
            #         var = [titleJournal]
            #         cursor.execute(query, var)
            #         journalID = cursor.fetchone()[0]
            #         sql = "UPDATE JOURNAL_ENTRY SET ENTRY_TEXT = %s WHERE JOURNAL_ID = %s AND ENTRY_TEXT " \
            #               "like %s"
            #         variables = [newtext, journalID, text]
            #         cursor.execute(sql, variables)
            #         # sss = "SELECT ENTRY_ID FROM JOURNAL_ENTRY WHERE ENTRY_TEXT like %s"
            #         # v = [newtext]
            #         # cursor.execute(sss, v)
            #         # entryID = cursor.fetchone()[0]
            #         # s = "UPDATE DATE_ENTRY SET DATE_FULL = %s WHERE ENTRY_ID = %s AND DATE_FULL = %s"
            #         cursor.connection.commit()
            #         # cursor.execute(s,[newdate,entryID,date])
            #         return HttpResponse("edited successfully")
                # except:
    else:
        #is journal entry
        objj=date+", "+text
    if request.method == 'POST':
        # newdate = request.POST.get('newdate')
        newtext = request.POST.get('newentry')
        with connection.cursor() as cursor:
            # try:
                query = "SELECT JOURNAL_ID FROM JOURNAL WHERE JOURNAL_TITLE = %s"
                var = [titleJournal]
                cursor.execute(query, var)
                journalID = cursor.fetchone()[0]
                sql = "UPDATE JOURNAL_ENTRY SET ENTRY_TEXT = %s WHERE JOURNAL_ID = %s AND ENTRY_TEXT " \
                      "like %s"
                variables = [newtext, journalID, text]
                cursor.execute(sql,variables)
                # sss = "SELECT ENTRY_ID FROM JOURNAL_ENTRY WHERE ENTRY_TEXT like %s"
                # v = [newtext]
                # cursor.execute(sss, v)
                # entryID = cursor.fetchone()[0]
                # s = "UPDATE DATE_ENTRY SET DATE_FULL = %s WHERE ENTRY_ID = %s AND DATE_FULL = %s"
                cursor.connection.commit()
                # cursor.execute(s,[newdate,entryID,date])
                return render(request, "success.html")
            # except:
            #     return HttpResponse("editing failed")
    return render(request, "editing.html",{'objj': objj})

#close cursor
#close connection
#but when?
def delete(request):
    table_name = ""
    titleOrfirstname=request.GET.get('titleOrfirstname')
    firstOrlastname=request.GET.get('firstOrlastname')
    centuryOrJournal=request.GET.get('centuryOrJournal')

    date=request.GET.get('date')
    text=request.GET.get('text')
    if date==None :
        if centuryOrJournal.isdigit():
            #is journal
            obj=titleOrfirstname #is title in this case
            table_name = "journal"
            # print("journal")
        else:
            #is author
            obj=titleOrfirstname + ", "+firstOrlastname #is first, lastname in this case
            table_name="author"
            # print("author")
    else:
        #is journal entry
        obj=date+", "+text
        table_name="journal_entry"
        # print("journal_entry")
    if request.method == 'POST':
        with connection.cursor() as cursor:
            try:
                if table_name == "journal":
                    sql = "DELETE FROM journal WHERE journal_title = %s AND century = %s"
                    variables = [titleOrfirstname,centuryOrJournal]
                    cursor.execute(sql, variables)
                    connection.commit()
                    return render(request, "success.html")
                elif table_name == "author":
                    sql = "DELETE FROM author WHERE auth_fname = %s AND auth_lname = %s"
                    variables = [titleOrfirstname,firstOrlastname]
                    cursor.execute(sql, variables)
                    connection.commit()
                    return render(request, "success.html")

                elif table_name == "journal_entry":
                    sql = "DELETE FROM journal_entry WHERE entry_text like %s"
                    variables = [text]
                    cursor.execute(sql, variables)
                    connection.commit()
                    return render(request, "success.html")

                return HttpResponse("error deleting")
            except:
                return HttpResponse("error deleting")
    return render(request, "delete.html",{'obj': obj})


def success(request):
    return HttpResponse("success!")