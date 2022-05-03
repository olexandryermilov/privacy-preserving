import json
import sys


def process_file(path):
    file = open(path, 'r')
    new_file = open("train_placeholders_spacy_translation.json", "w")
    lines = file.readlines()
    new_file.write('{"data":[')
    for line in lines[:-1]:
        print(line[:-1])
        obj = json.loads(line[:-2])
        new_file.write('{"translation": {"en":"' + obj['text'] +'", "de":"'+ obj['summary']+'"}},')
    for line in lines[-1:]:
        obj = json.loads(line)
        new_file.write('{"translation": {"en":"' + obj['text'] + '", "de":"' + obj['summary'] + '"}}')
    new_file.write(']}')


process_file(sys.argv[1])