# Bridget Kim xpt3bn
import re
import openpyxl

#check file type, if xlsx give option to select column numbers
#if txt, say its not guaranteed to be correct but it will try
#will only do journals so has to have dates

century = 17
def parseFile():
    pass
#or whatever they lived through
def parse_text_file(file_path):
    try:
        counter = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if extract_dates(line, century):
                    counter+=1
                    print(line)

        print(counter)
                # print(line.strip())  # Print each line (remove leading/trailing whitespace)

    except FileNotFoundError:
        print(f"File not found: {file_path}")



def extract_dates(text, century):
    # pattern = r"\d{1,2}, \b\d{4}"
    pattern = r"[.,]\s" + str(century) + r"\d{2}\b"
    dates = re.findall(pattern, text)
    if len(dates) != 0:
        return True
    return False




def parse_excel_file(file_path, column_indexes=None):
    wb = openpyxl.load_workbook(file_path)  # Load the Excel file
    sheet = wb.active  # Select the active sheet (or specify a specific sheet name)

    data = []  # List to store the parsed data
    #journal date, location = sites, notes, sites, sketch,  country=italy

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

# filepath = "C:/Users/bridg/Downloads/Italian_Journey_Rome_Naples_clean.txt"
# filepath = "C:/Users/bridg/Downloads/ItalianJourney1786-1788onlyentries(1).txt"
file_path = "C:/Users/bridg/Downloads/Goethe_Italian_JourneyDRIVEDOC.xlsx"
# parse_text_file(filepath)

column_indexes = [1, 2,10,16,31]
parsed_data = parse_excel_file(file_path, column_indexes)

# Separate arrays for each row
rows = parsed_data
del rows[0]
for row in rows:
    print(row)
#if no day, then check before entry and after entry and make it equal to that
#check every paragraph's first line for a date