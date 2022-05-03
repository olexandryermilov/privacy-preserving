import json
import sys
from tqdm import tqdm

def process_file(path):
    file = open(path, 'r')
    new_file = open("train_placeholders_spacy_translation.json", "w")
    lines = file.readlines()
    new_file.write('{"data":[\n')
    s = '{"text": "iron cement is a ready for use paste which is laid as a fillet by putty knife or finger in the mould edges ( corners ) of the steel ingot mould .","summary": "iron cement ist eine gebrauchs # # MISC_1 # # fertige Paste , die mit einem Spachtel oder den LOC_1 als Hohlkehle in die Formecken ( Winkel ) der MISC_2 MISC_3 aufgetragen wird ."}'
    obj = json.loads(s)
    new_file.write('{"translation": {"en":"' + obj['text'] + '", "de":"' + obj['summary'] + '"}},\n')
    for line in tqdm(lines[1:-1]):
        obj = json.loads(line[:-2])
        new_file.write('{"translation": {"en":"' + obj['text'] +'", "de":"'+ obj['summary']+'"}},\n')
    for line in lines[-1:]:
        obj = json.loads(line)
        new_file.write('{"translation": {"en":"' + obj['text'] + '", "de":"' + obj['summary'] + '"}}\n')
    new_file.write(']}')


process_file(sys.argv[1])