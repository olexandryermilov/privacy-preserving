import sys

import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import csv
from tqdm import tqdm
import json

model = AutoModelForTokenClassification.from_pretrained("Davlan/xlm-roberta-large-ner-hrl")
tokenizer = AutoTokenizer.from_pretrained("Davlan/xlm-roberta-large-ner-hrl")

ner_model = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy = "simple")

entity_map = dict()
placeholders_map = dict()
def readFile(filePath):
  f = open(filePath, "r")
  return f.read()

def writeFileCSV(filePath, content):
    f = open(filePath, "w")
    f.write("text,summary\n")
    for e in content:
        f.write(e[0] + ',' + e[1] + "\n")
    f.close()

def obtain_named_entities(text):
  return ner_model(text)

def replaceNEWithEntityGroup(text, parsed_named_entities):
  anonymizedText = text
  for entity in reversed(parsed_named_entities):
    start = entity['start']
    end = entity['end']
    entity_word = entity['word']
    if entity_word not in entity_map:
      entity_type = entity['entity_group']
      if entity_type not in placeholders_map:
        placeholders_map[entity_type] = 1
      else:
        placeholders_map[entity_type] = placeholders_map[entity_type] + 1
      entity_map[entity_word] = entity_type + "_" + str(placeholders_map[entity_type])
    replacement = entity_map[entity_word]
    anonymizedText = anonymizedText[:start+1] + replacement + anonymizedText[end:]
  return anonymizedText


def anonymizeCorpus(corpus):
  named_entities = obtain_named_entities(corpus)
  anonymized_corpus = replaceNEWithEntityGroup(corpus, named_entities)
  return anonymized_corpus


def closestWord2Vec(corpus):
    named_entities = obtain_named_entities(corpus)

def writeFileJSONAnon(filePath, content, anonFunc):
    f = open(filePath, "a")
    f.write('{"data":[')
    f.close()
    for e in tqdm(content[:-1]):
        f = open(filePath, "a")
        f.write('{"text": "' + anonFunc(e[0].replace('"', '').replace('\\','').replace('\t','')) + '","summary": "' + anonFunc(e[1].replace('"', '').replace('\\','').replace('\t','')) + '"},\n')
        f.close()
    f = open(filePath, "a")
    for e in content[-1:]:
        f.write(
            '{"text": "' + anonFunc(e[0].replace('"', '').replace('\\', '').replace('\t', '')) + '","summary": "' + anonFunc(e[1].replace(
                '"', '').replace('\\', '').replace('\t', '')) + '"}\n')

    f.write(']}')
    f.close()

def writeFileJSON(filePath, content):
    f = open(filePath, "w")
    f.write('{"data":[')
    for e in tqdm(content[:-1]):
        f.write('{"text": "' + e[0].replace('"', '').replace('\\','').replace('\t','') + '","summary": "' + e[1].replace('"', '').replace('\\','').replace('\t','') + '"},\n')
    for e in content[-1:]:
        f.write(
            '{"text": "' + e[0].replace('"', '').replace('\\', '').replace('\t', '') + '","summary": "' + e[1].replace(
                '"', '').replace('\\', '').replace('\t', '') + '"}\n')

    f.write(']}')
    f.close()

def processFile(filePath, fileName, anonymize, methodFunc, methodName):
    source = readFile(filePath + fileName + '.source').split("\n")
    target = readFile(filePath + fileName + '.target').split("\n")
    together = list(zip(source, target))
    if anonymize:
        writeFileJSONAnon(filePath+fileName+"_anonymized_"+methodName+".json", together, methodFunc)
    else:
        writeFileJSON(filePath+fileName+".json", together)
    return


def main():
    path = sys.argv[1]
    if sys.argv[2] == 'anon':
        methodName = sys.argv[3]
        if methodName == 'ner-placeholder':
            method = anonymizeCorpus
        processFile(path, 'train', True, method, methodName)
        processFile(path,  'test', True, method, methodName)
        processFile(path,   'val', True, method, methodName)
        if methodName == 'ner-placeholder':
            with open('placeholders.json', 'wb') as f:
                json.dump(placeholders_map, f)
    else:
        processFile(path, 'train')
        processFile(path, 'test')
        processFile(path, 'val')

main()