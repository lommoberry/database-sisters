import openpyxl
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
import re
from datetime import datetime


def entry_parser_findNotes(entry):
    note_pattern = r"\[Sidenote:\s(.*)\]"
    note_matches = re.findall(note_pattern, entry)
    sidenote_content = ""
    for match in note_matches:
        sidenote_content += match.strip() + ", "

    return sidenote_content.upper()


def entry_parser_findCity(entry):
    pattern = r"_(.*?), (.*?_\s\d{1,2}, \d{4})"
    matches = re.findall(pattern, entry)
    city = ""
    for match in matches:
        city = match[0]
    return city.upper()

def entry_parser_findSites(entry):
    words = nltk.word_tokenize(entry)
    tagged_words = nltk.pos_tag(words)
    entities = nltk.chunk.ne_chunk(tagged_words)
#ORG = organization, PER = person, GPE=Geo politicla entity, LOC=location, DATE, TIME, MONEY, PERCENT, FACILITY
    locations = []
    string = ""
    for entity in entities:
        if hasattr(entity, 'label') and (entity.label() == 'GPE' or entity.label() == 'LOC'):
            locations.append(', '.join(word for word, tag in entity.leaves()))
    for i in range(len(locations)):
        string += locations[i].upper() + ", "
    return string



def raw_date_cleaner(date_raw):
    abbreviations = {
        'JAN.': 'JANUARY',
        'FEB.': 'FEBRUARY',
        'MAR.': 'MARCH',
        'APR.': 'APRIL',
        'JUN.': 'JUNE',
        'JUL.': 'JULY',
        'AUG.': 'AUGUST',
        'SEPT.': 'SEPTEMBER',
        'OCT.': 'OCTOBER',
        'NOV.': 'NOVEMBER',
        'DEC.': 'DECEMBER'
    }
    pattern = r"_(.*?), (.*?_\s\d{1,2}, \d{4})"
    matches = re.findall(pattern, date_raw)
    date = ""
    for match in matches:
        date = match[1]

    if date == "":
        return None
    if date.startswith("_"):
        date = date[1:]
    pattern2 = r'\b(' + '|'.join(abbreviations.keys()) + r')\b'

    def replace_month(match):
        if match:
            return abbreviations[match.group()]
        return match.group()

    date = re.sub(pattern2, replace_month, date)
    # print(date)
    date_str = date.strip()  # Remove newline character
    # print(date_str)
    date_obj = datetime.strptime(date_str, "%B_ %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")

    return formatted_date

def excelMaker(journalTitle):
    # Create a new workbook
    workbook = openpyxl.Workbook()

    # Select the active sheet
    sheet = workbook.active

    # Write data to cells
    sheet['A1'] = 'DATE'
    sheet['B1'] = 'ENTRY'
    sheet['C1'] = 'LOCATIONS'
    sheet['D1'] = 'SKETCHES'
    sheet['E1'] = 'NOTES'
    sheet['F1'] = 'CITY'

    entry_array =[]
    text = ""

    pattern = r"\b\w+ \d{1,2}, \d{4}\b"

    dates_raw=[]
    file_path = 'C:/Users/bridg/Downloads/Goethe_clean_italy.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                if text:
                    entry_array.append(text.strip())
                    text = ""
                dates_raw.append(line.upper())
            text += line

    file.close()
    entry_array.pop(0)
    num_rows = len(entry_array)
    #add in things
    for row in range(1, num_rows+1):
        entry = entry_array[row-1]
        for col in range(1,7):
            cell = sheet.cell(row=row,column=col)
            if col==1:
                #date
                # print(row,col)
                cell.value = raw_date_cleaner(dates_raw[row-1])
                pass
            elif col==2:
                #entry
                # print(row, col)
                cell.value = entry
                pass
            elif col==3:
                #locations
                # print(row, col)
                cell.value = entry_parser_findSites(entry)
                pass
            elif col==4:
                #sketches
                # print(row, col)
                cell.value = None
                pass
            elif col==5:
                #notes
                # print(row, col)
                cell.value = entry_parser_findNotes(entry)
                pass
            elif col==6:
                #city
                # print(row, col)
                cell.value = entry_parser_findCity(entry)
                pass
            else:
                pass

    # Save the workbook
    workbook.save(journalTitle + '.xlsx')
