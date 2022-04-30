
import sys
from tqdm import tqdm
import json

import spacy

NER = spacy.load("en_core_web_sm")
DE_NER = spacy.load("de_core_news_sm")

entity_map = dict()
placeholders_map = dict()


total = 0
def readFile(filePath):
  f = open(filePath, "r")
  return f.read()

def writeFileCSV(filePath, content):
    f = open(filePath, "w")
    f.write("text,summary\n")
    for e in content:
        f.write(e[0] + ',' + e[1] + "\n")
    f.close()

def anonymizeCorpus(corpus, f, ner):
  processed = ner(corpus)
  res = []
  result = 0
  for entity in processed:
      if entity.ent_type_:
          result += 1
          entity_word = entity.text
          if entity_word not in entity_map:
              entity_type = entity.ent_type_
              if entity_type not in placeholders_map:
                  placeholders_map[entity_type] = 1
              else:
                  placeholders_map[entity_type] = placeholders_map[entity_type] + 1
              entity_map[entity_word] = entity_type + "_" + str(placeholders_map[entity_type])
          replacement = entity_map[entity_word]
          res.append(replacement)
      else:
          res.append(entity.text)
  write(f, " ".join(res))
  return result

def write(f, text):
    f.write(text)
    return

def writeFileJSONAnon(filePath, content, anonFunc, task):
    f = open(filePath, "a")
    f.write('{"data":[')
    f.close()
    result = 0
    if task == "summarization":
        ner_source = NER
        ner_target = NER
    elif task == "translation":
        ner_source = NER
        ner_target = DE_NER
    else:
        ner_source = NER
        ner_target = NER

    for e in tqdm(content[:-1]):
        f = open(filePath, "a")
        f.write('{"text": "')
        result += anonFunc(e[0].replace('"', '').replace('\\','').replace('\t',''), f, ner_source)
        f.write('","summary": "')
        result += anonFunc(e[1].replace('"', '').replace('\\','').replace('\t',''), f, ner_target)
        f.write('"},\n')
        #f.write('{"text": "' + anonFunc(e[0].replace('"', '').replace('\\','').replace('\t','')) + '","summary": "' + anonFunc(e[1].replace('"', '').replace('\\','').replace('\t','')) + '"},\n')
        f.close()
    f = open(filePath, "a")
    for e in content[-1:]:
        f = open(filePath, "a")
        f.write('{"text": "')
        anonFunc(e[0].replace('"', '').replace('\\', '').replace('\t', ''), f, ner_source)
        f.write('","summary": "')
        anonFunc(e[1].replace('"', '').replace('\\', '').replace('\t', ''), f, ner_target)
        f.write('"}\n')

    f.write(']}')
    f.close()
    with open("all_ners.txt","w") as f1:
        f1.write(str(result/len(content)))


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

def processFile(filePath, fileName, anonymize, methodFunc, methodName, task):
    source = readFile(filePath + fileName + '.source').split("\n")
    target = readFile(filePath + fileName + '.target').split("\n")
    together = list(zip(source, target))
    if anonymize:
        writeFileJSONAnon(filePath+fileName+"_anonymized_spacy1_"+methodName+".json", together, methodFunc, task)
    else:
        writeFileJSON(filePath+fileName+".json", together)
    return

def main():

    path = sys.argv[1]
    if len(sys.argv)>2 and sys.argv[2] == 'anon':
        methodName = sys.argv[3]
        task = sys.argv[4]
        if methodName == 'ner-placeholder':
            method = anonymizeCorpus
        processFile(path, 'train1', True, method, methodName, task)
        processFile(path,  'test', True, method, methodName, task)
        processFile(path,   'val', True, method, methodName, task)
        if methodName == 'ner-placeholder':
            with open(f'placeholders_spacy_{task}.json', 'w') as f:
                f.write(json.dumps(entity_map))
    else:
        processFile(path, 'train', False, None, "", "")
        processFile(path, 'test', False, None, "", "")
        processFile(path, 'val', False, None, "", "")
main()