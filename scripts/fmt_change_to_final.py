#!/usr/bin/env python

import os
import sys
from pathlib import Path
import json
import math

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DEBUG = False
dirs = [os.path.join('json_pair_slides', 'CS-0441 Lecture Slides'),
  os.path.join('json_pair_slides', 'CS-0449 Lecture Slides'),
  os.path.join('json_pair_slides', 'CS-1541 Lecture Notes'),
  os.path.join('json_pair_slides', 'CS-1550 Lecture Slides'),
  os.path.join('json_pair_slides', 'CS-1567 Lecture Notes'),
  os.path.join('json_pair_slides', 'CS-1622 Lecture Slides')]

dirs = [os.path.join('json_pair_slides', 'CS-1541 Lecture Notes')]

import argparse

text='''{
    "1": [
        {
            "word": "The",
            "label": "O"
        },
        {
            "word": "Operating",
            "label": "B"
        },
        {
            "word": "System",
            "label": "I"
        },
        {
            "word": "uses",
            "label": "O"
        },
        {
            "word": "Interrupts",
            "label": "B"
        },
        {
            "word": "to",
            "label": "O"
        },
        {
            "word": "implement",
            "label": "O"
        },
        {
            "word": "System",
            "label": "B"
        },
        {
            "word": "Calls",
            "label": "I"
        }
    ],
    "2": [
        {
            "word": "Interrupts",
            "label": "B"
        },
        {
            "word": "are",
            "label": "O"
        },
        {
            "word": "handled",
            "label": "O"
        },
        {
            "word": "using",
            "label": "O"
        },
        {
            "word": "interrupt",
            "label": "B"
        },
        {
            "word": "service",
            "label": "I"
        },
        {
            "word": "routines",
            "label": "I"
        },
        {
            "word": "(",
            "label": "O"
        },
        {
            "word": "ISRs",
            "label": "B"
        },
        {
            "word": ")",
            "label": "O"
        }
    ],
    "3": [],
    "4": [],
    "5": [
        {
            "word": "\u2022",
            "label": "O"
        },
        {
            "word": "ISRs",
            "label": "B"
        },
        {
            "word": "are",
            "label": "O"
        },
        {
            "word": "segments",
            "label": "O"
        },
        {
            "word": "of",
            "label": "O"
        },
        {
            "word": "code",
            "label": "O"
        },
        {
            "word": "that",
            "label": "O"
        },
        {
            "word": "determine",
            "label": "O"
        },
        {
            "word": "what",
            "label": "O"
        }
    ],
    "6": [
        {
            "word": "action",
            "label": "O"
        },
        {
            "word": "should",
            "label": "O"
        },
        {
            "word": "be",
            "label": "O"
        },
        {
            "word": "taken",
            "label": "O"
        },
        {
            "word": "for",
            "label": "O"
        },
        {
            "word": "each",
            "label": "O"
        },
        {
            "word": "type",
            "label": "O"
        },
        {
            "word": "of",
            "label": "O"
        },
        {
            "word": "interrupt",
            "label": "B"
        }
    ],
    "7": [
        {
            "word": "\u2022",
            "label": "O"
        },
        {
            "word": "part",
            "label": "O"
        },
        {
            "word": "of",
            "label": "O"
        },
        {
            "word": "the",
            "label": "O"
        },
        {
            "word": "OS",
            "label": "B"
        },
        {
            "word": "kernel",
            "label": "B"
        }
    ]
}'''

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
    index = 0
    prev_blank = False
    json_parr_together = [{'words': [], 'labels': []}]
    for parr in json_parr:
        if len(json_parr[parr]['words']) == 0:
            if prev_blank:
                index+=1
                print(index)
                json_parr_together.append({'words': [], 'labels': []})
            prev_blank = not prev_blank
        print(index)
        json_parr_together[index]['words'].extend(json_parr[parr]['words'])
        json_parr_together[index]['labels'].extend(json_parr[parr]['labels'])                
    return json_parr_together

if DEBUG:
    mx=0
    for dir in dirs:
        files = Path(dir).glob('**/*.json')
        for file in files:
            with open(file, 'rb') as f:
                
                """nwdir = os.path.join(ROOT_DIRECTORY, "final_slides_json", Path(dir).stem)
                print(nwdir)
                try:
                    os.mkdir(nwdir)
                except Exception as e:
                    print(e)
                    pass
                print(file)
                """
                text = f.read()
                processed = json.loads(text)
                pair = convert_to_parr(processed)
                for item in pair:
                    mx = max(mx, len(item["words"]))
                """
                with open(os.path.join(nwdir, Path(file).stem)+".json", 'w') as f2:
                    f2.write(json.dumps(pair, indent=4))
                """
    print(f"the max slide tokens is {mx}")
else:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help = "File Input", type=Path)
    parser.add_argument("-o", "--output", help = "File Output", type=Path)
    args = parser.parse_args(sys.argv[1:])

    if args.file:
        with open(args.file, 'rb') as f:
            text = f.read()
    processed = json.loads(text)
    pair = convert_to_parr(processed)
    if args.output:
        with open(args.output, 'w') as f2:
            f2.write(json.dumps(pair, indent=4))