import os

import sys
from flair.models import SequenceTagger
from flair.data import Sentence
from segtok.segmenter import split_single
from tqdm import tqdm
import json

tagger = SequenceTagger.load('flair/ner-english-ontonotes-fast')

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

def anonymizeCorpus(corpus):
  sentences = [Sentence(sent, use_tokenizer=False) for sent in split_single(corpus)]
  tagger.predict(sentences)
  anonymizedTextAll = ""
  for sent in sentences:
      anonymizedText = sent.text.replace(" '","'")
      diff = 0
      for entity in sent.get_spans('ner'):
          start = entity.start_position
          end = entity.end_position
          entity_word = entity.text
          if entity_word not in entity_map:
              entity_type = entity.get_label("ner").value
              if entity_type not in placeholders_map:
                  placeholders_map[entity_type] = 1
              else:
                  placeholders_map[entity_type] = placeholders_map[entity_type] + 1
              entity_map[entity_word] = entity_type + "_" + str(placeholders_map[entity_type])
          replacement = entity_map[entity_word]
          anonymizedText = anonymizedText[:start - diff] + replacement + anonymizedText[end - diff:]
          diff += len(entity.text) - len(replacement)
      anonymizedTextAll = anonymizedTextAll + anonymizedText
  return anonymizedTextAll

def write(f, text):
    f.write(text)
    return

import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def anonymizeCorpusTesting(corpus, f):
  sentences = [Sentence(sent, use_tokenizer=False) for sent in split_into_sentences(corpus)]
  tagger.predict(sentences)
  for sent in sentences:
      anonymizedText = sent.text.replace(" '","'")
      diff = 0
      #for entity in sent.get_spans('ner'):
      #    start = entity.start_position
      #    end = entity.end_position
      #    entity_word = entity.text
          #if entity_word not in entity_map:
          #    entity_type = entity.get_label("ner").value
          #    if entity_type not in placeholders_map:
          #        placeholders_map[entity_type] = 1
          #    else:
          #        placeholders_map[entity_type] = placeholders_map[entity_type] + 1
          #    entity_map[entity_word] = entity_type + "_" + str(placeholders_map[entity_type])
          #replacement = entity_map[entity_word]
          #write(f, anonymizedText[:start - diff])
          #write(f, replacement)
          #write(f, anonymizedText[end - diff:])
          #diff += len(entity.text) - len(replacement)
  return


def calcNer(corpus):
  sentences = [Sentence(sent, use_tokenizer=False) for sent in split_single(corpus)]
  tagger.predict(sentences)
  result = 0
  for sent in sentences:
    result += len(sent.get_spans('ner'))
  return result

def calcAllNer(content):
    i = 0
    result = 0
    for e in tqdm(content):
        i += 1
        result += calcNer(e)
        print(f"together = {result}, average = {result/i} ")


def writeFileJSONAnon(filePath, content, anonFunc):
    f = open(filePath, "a")
    f.write('{"data":[')
    f.close()
    for e in tqdm(content[:-1]):
        f = open(filePath, "a")
        f.write('{"text": "')
        anonFunc(e[0].replace('"', '').replace('\\','').replace('\t',''), f)
        f.write('","summary": "')
        anonFunc(e[1].replace('"', '').replace('\\','').replace('\t',''), f)
        f.write('"},\n')
        #f.write('{"text": "' + anonFunc(e[0].replace('"', '').replace('\\','').replace('\t','')) + '","summary": "' + anonFunc(e[1].replace('"', '').replace('\\','').replace('\t','')) + '"},\n')
        f.close()
    f = open(filePath, "a")
    for e in content[-1:]:
        f = open(filePath, "a")
        f.write('{"text": "')
        anonFunc(e[0].replace('"', '').replace('\\', '').replace('\t', ''), f)
        f.write('","summary": "')
        anonFunc(e[1].replace('"', '').replace('\\', '').replace('\t', ''), f)
        f.write('"}\n')

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


def main1():
    source = readFile('train.source').split("\n")
    calcAllNer(source)


def main():
    path = sys.argv[1]
    if len(sys.argv)>2 and sys.argv[2] == 'anon':
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
        processFile(path, 'train', False, None, "")
        processFile(path, 'test', False, None, "")
        processFile(path, 'val', False, None, "")
main()