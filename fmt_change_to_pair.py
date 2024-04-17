#!/usr/bin/env python

import os
from pathlib import Path
import json
import argparse
import sys

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DEBUG =  True

dirs = [os.path.join('json_slides', 'CS-0441 Lecture Slides'),
  os.path.join('json_slides', 'CS-0449 Lecture Slides'),
  os.path.join('json_slides', 'CS-1541 Lecture Notes'),
  os.path.join('json_slides', 'CS-1550 Lecture Slides'),
  os.path.join('json_slides', 'CS-1567 Lecture Notes'),
  os.path.join('json_slides', 'CS-1622 Lecture Slides')]



def convert_to_pair(json_parr):
    json_pair = {}
    for parr in json_parr:
        try:
            json_pair[parr] = [{'word': json_parr[parr]['words'][i], 'label': json_parr[parr]['labels'][i]} for i in range(len(json_parr[parr]['words']))]
        except IndexError:
            print(parr)
            exit()
    return json_pair
def convert_to_parr(json_pair):
    json_parr = {}
    for pair in json_pair:
        json_parr[pair] = {'words': [json_pair[pair][i]['word'] for i in range(len(json_pair[pair]))], 'labels': [json_pair[pair][i]['label'] for i in range(len(json_pair[pair]))]}
    return json_parr

if not DEBUG:
    directory = 'json_pair_slides'
    #for dir in Path(directory).glob('*'): # if you want to do it on all data in json_slides...
    for dir in dirs:
        files = Path(dir).glob('**/*.json')
        for file in files:
            with open(file, 'rb') as f:
                nwdir = os.path.join(ROOT_DIRECTORY, "json_pair_slides", Path(dir).stem)
                print(nwdir)
                try:
                    os.mkdir(nwdir)
                except Exception as e:
                    pass
                print(file)
                text = f.read()
                processed = json.loads(text)
                pair = convert_to_pair(processed)
                with open(os.path.join(nwdir, Path(file).stem)+".json", 'w') as f2:
                    f2.write(json.dumps(pair, indent=4))
else:

    text = """
   {
"1": {
"words": ["The", "Operating", "System", 
    "uses", "Interrupts", "to",
    "implement", "System", "Calls"], 
"labels": ["O", "B", "I",
    "O", "B", "O",
    "O", "B", "I"]
},
"2": {
"words": ["Interrupts", "are", "handled",
    "using", "interrupt", "service", 
    "routines", "(", "ISRs", ")"],
"labels": ["B", "O", "O",
    "O", "B", "I",
    "I", "O", "B", "O"]
},
"3": {
   "words": [],
   "labels": []
},
"4": {
    "words": [],
    "labels": []
},
"5": {
"words": ["\u2022", "ISRs", "are", 
        "segments", "of", "code",
        "that", "determine", "what"],
"labels": ["O", "B", "O",
        "O", "O", "O",
        "O", "O", "O"]
},
"6": {
"words": ["action", "should", "be",
        "taken", "for", "each",
        "type", "of", "interrupt"],
"labels": ["O", "O", "O",
        "O", "O", "O",
        "O", "O", "B"]
},
"7": {
"words": ["\u2022", "part", "of",
        "the", "OS", "kernel"],
"labels": ["O", "O", "O",
          "O", "B", "B"]
}
}
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "File Input", type=Path)
    parser.add_argument("-o", "--output", help = "File Output", type=Path)
    args = parser.parse_args(sys.argv[1:])

    if args.file:
        with open(args.file, 'rb') as f:
            text = f.read()
    processed = json.loads(text)
    pair = convert_to_pair(processed)
    if args.output:
        with open(args.output, 'w') as f2:
            f2.write(json.dumps(pair, indent=4))