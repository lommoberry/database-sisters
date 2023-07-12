# Bridget Kim xpt3bn
import openpyxl
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
import re
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

def raw_date_cleaner(date_raw):
    words = word_tokenize(date_raw)
    tagged_words = pos_tag(words)
    date = ''
    for i in range(len(tagged_words)):
        if tagged_words[i][1] == 'CD':
            date = tagged_words[i][0]
            break
    if date:
        # print(date)
        date_str = date.strip()  # Remove newline character
        # Parse the input date string using datetime
        parsed_date = datetime.strptime(date_str, "%B, %Y-%m-%d")
        # Format the date as MM-DD-YYYY
        formatted_date = parsed_date.strftime("%m-%d-%Y")
        return formatted_date
    else:
        return None


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


def arrayMaker(file_path):
    entry_array =[]
    dates_raw=[]
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    file.close()

    sentences = nltk.sent_tokenize(text)

    # Process each sentence
    current_entry = ""
    for sentence in sentences:
        # Tokenize words and perform named entity recognition (NER)
        words = nltk.word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        entities = nltk.chunk.ne_chunk(tagged_words)

        # Find date names from the named entities
        dates = []
        for entity in entities:
            if isinstance(entity, nltk.tree.Tree) and entity.label() == 'DATE':
                dates.append(' '.join([leaf[0] for leaf in entity.leaves()]))

        # If a date is found, start a new journal entry
        if dates:
            # Add the current entry to the result if not empty
            if current_entry:
                entry_array.append(' '.join(current_entry).strip())

            # Start a new entry with the date
            current_entry = [f"{dates[0]} {sentence}"]
        else:
            # Append the sentence to the current entry
            current_entry.append(sentence)

    # Add the last entry to the result if not empty
    if current_entry:
        entry_array.append(' '.join(current_entry).strip())


    num_rows = len(entry_array)
    array = [[0] * 6 for _ in range(num_rows)]
    #add in things
    for row in range(num_rows):
        entry = entry_array[row]
        for col in range(6):
            if col==1:
                #date
                # print(row,col)
                array[row][col] = raw_date_cleaner(dates_raw[row-1])
                pass
            elif col==2:
                #entry
                # print(row, col)
                array[row][col] = entry
                pass
            elif col==3:
                #locations
                # print(row, col)
                array[row][col] = entry_parser_findSites(entry)
                pass
            elif col==4:
                #sketches
                # print(row, col)
                array[row][col] = None
                pass
            elif col==5:
                #notes
                # print(row, col)
                array[row][col] = entry_parser_findNotes(entry)
                pass
            elif col==6:
                #city
                # print(row, col)
                array[row][col] = entry_parser_findCity(entry)
                pass
            else:
                pass

