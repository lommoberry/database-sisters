# Bridget Kim xpt3bn
import re
import openpyxl

#check file type, if xlsx give option to select column numbers
#if txt, say its not guaranteed to be correct but it will try
#will only do journals so has to have dates

century = 18
yearstart = century-1
def parseFile():
    pass
#or whatever they lived through
def parse_text_file(file_path):
    try:
        counter = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if extract_dates(line, yearstart):
                    counter+=1
                    print(line)

        print(counter)
                # print(line.strip())  # Print each line (remove leading/trailing whitespace)

    except FileNotFoundError:
        print(f"File not found: {file_path}")



def extract_dates(text, yearstart):
    # pattern = r"\d{1,2}, \b\d{4}"
    pattern = r"[.,]\s" + str(yearstart) + r"\d{2}\b"
    dates = re.findall(pattern, text)
    if len(dates) != 0:
        return True
    return False

def makeExcel(century):

