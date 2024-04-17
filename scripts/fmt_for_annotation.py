#!/usr/bin/env python

import pdftotext
import os
from nltk.tokenize import word_tokenize
from pathlib import Path
import json
import argparse
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Read PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        #reader = PyPDF2.PdfReader(file)
        #text = "\n".join([page.extract_text() for page in reader.pages])
        pdf = pdftotext.PDF(file)
        text = "\n\n".join(pdf)
    print(text)
    return text

def dummy_json(text):
    count = 1
    json_dict = {}
    for line in str.split(text, sep='\n'):
        words = word_tokenize(line)
        json = {'words': words, 'labels': ['O' for i in range(len(words))]}
        json_dict[count] = json
        count += 1
    return json_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "File Input", type=Path)
    parser.add_argument("-t", "--text", help = "Text Output", type=Path)
    parser.add_argument("-j", "--json", help = "Json Output", type=Path)
    args = parser.parse_args(sys.argv[1:])

    text = read_pdf(file_path=args.file)
    with open(args.text, 'w') as f:
        f.write(text)
    dummy_json_text = dummy_json(text)
    with open(args.json, 'w') as f:
        f.write(json.dumps(dummy_json_text, indent=4))
            


