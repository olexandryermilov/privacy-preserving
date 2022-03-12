import os

from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import sys

model = AutoModelForTokenClassification.from_pretrained("Davlan/xlm-roberta-large-ner-hrl")
tokenizer = AutoTokenizer.from_pretrained("Davlan/xlm-roberta-large-ner-hrl")

ner_model = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy = "simple")

def readFile(filePath):
  f = open(filePath, "r")
  return f.read()

def overwriteFile(filePath, newContent):
  f = open(filePath, "w")
  f.write(newContent)
  f.close()

def obtain_named_entities(text):
  return ner_model(text)

def replaceNEWithEntityGroup(text, parsed_named_entities):
  anonymizedText = text
  entity_map = dict()
  placeholders_map = dict()
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
  overwriteFile(filePath, corpus)
  return anonymized_corpus

def main():
    args = sys.argv[1:]
    for file in os.listdir(args[0]):
      anonymizeCorpus(file)

if __name__ == "__main__":
    main()