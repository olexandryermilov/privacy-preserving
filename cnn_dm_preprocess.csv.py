import sys

import pandas as pd
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import csv

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


def anonymizeCorpus(filePath):
  corpus = readFile(filePath)
  named_entities = obtain_named_entities(corpus)
  anonymized_corpus = replaceNEWithEntityGroup(corpus, named_entities)
  return anonymized_corpus

def writeFileJSON(filePath, content):
    f = open(filePath, "w")
    f.write('{"data":[')
    for e in content[:-1]:
        f.write('{"text": "' + e[0].replace('"', '').replace('\\','').replace('\t','') + '","summary": "' + e[1].replace('"', '').replace('\\','').replace('\t','') + '"},\n')
    for e in content[-1:]:
        f.write(
            '{"text": "' + e[0].replace('"', '').replace('\\', '').replace('\t', '') + '","summary": "' + e[1].replace(
                '"', '').replace('\\', '').replace('\t', '') + '"}\n')

    f.write(']}')
    f.close()

def processFileWithAnonymize(filePath, fileName):
    source = anonymizeCorpus(readFile(filePath + fileName + '.source')).split("\n")
    target = anonymizeCorpus(readFile(filePath + fileName + '.target')).split("\n")
    together = list(zip(source, target))
    #df = pd.DataFrame(data = together, columns = ["text", "summary"])
    #df.to_csv(fileName + '.csv', index = False,quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")
    writeFileJSON(filePath+fileName+"_anonymized.json", together)
    return

def processFile(filePath, fileName):
    source = (readFile(filePath + fileName + '.source')).split("\n")
    target = (readFile(filePath + fileName + '.target')).split("\n")
    together = list(zip(source, target))
    #df = pd.DataFrame(data = together, columns = ["text", "summary"])
    #df.to_csv(fileName + '.csv', index = False,quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")
    writeFileJSON(filePath+fileName+".json", together)
    return

def main():
    path = sys.argv[1]
    if sys.argv[2] == 'anon':
        processFileWithAnonymize(path, 'train')
        processFileWithAnonymize(path, 'test')
        processFileWithAnonymize(path, 'val')
    else:
        processFile(path, 'train')
        processFile(path, 'test')
        processFile(path, 'val')

main()