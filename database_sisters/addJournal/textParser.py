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



def arrayMaker(file_path, century):
    entry_array =[]
    dates = []
    text = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                match = parser.parse(line, fuzzy_with_tokens=True)
                if match:
                    for i in century:
                        year = str(i-1)
                        date= str(match[0].date())
                        if date.startswith(year):
                            entry_array.append(text.strip())
                            text = ""
                            dates.append(date)
                            pass

            except:
                text += line
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

