# Bridget Kim xpt3bn
import re
import openpyxl

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
#date, entry, locations, sketch, note, city
    column_indexes = [date, entry, locations, sketch, note, city]
    parsed_data = parse_excel_file(file, column_indexes)

# Separate arrays for each row
    rows = parsed_data
    return rows
# if no day, then check before entry and after entry and make it equal to that
# check every paragraph's first line for a date
# Bridget Kim xpt3bn
# file_path = "/database_sisters/justPlayin/3.xlsx"
# runExcelReader(file_path, 0, 1, 2, 3, 4, 5)