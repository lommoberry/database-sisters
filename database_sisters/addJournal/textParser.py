# Bridget Kim xpt3bn
import re

def parse_text_file(file_path):
    try:
        counter = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if extract_dates(line):
                    counter+=1
                    print(line)

        print(counter)
                # print(line.strip())  # Print each line (remove leading/trailing whitespace)

    except FileNotFoundError:
        print(f"File not found: {file_path}")



def extract_dates(text):
    pattern = r"\d{1,2}, \b\d{4}"
    dates = re.findall(pattern, text)
    if len(dates) != 0:
        return True
    return False

filepath = "C:/Users/bridg/Downloads/Italian_Journey_Rome_Naples_clean.txt"
parse_text_file(filepath)