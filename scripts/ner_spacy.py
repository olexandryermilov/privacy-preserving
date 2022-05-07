import sys
from tqdm import tqdm
import json
import numpy as np

import spacy

NER = spacy.load("en_core_web_sm")
DE_NER = spacy.load("de_core_news_sm")

entity_map = dict()
placeholders_map = dict()

total = 0

def readPlaceholderMap():
    with open("../files/placeholders_spacy.json", "r") as file:
        entities = dict()
        data = json.load(file)
        for k in tqdm(data):
            splitted = data[k].split("_")
            entity = "_".join(splitted[0:-1])
            num = int(splitted[-1])
            if entity in entities:
                entities[entity] = max(entities[entity], num)
            else:
                entities[entity] = num
        return data, entities

def numFromPlaceholder(placeholder):
    return int(placeholder.split("_")[-1])

def createPermutationsForEntities(entities):
    permutations = dict()
    for k in entities:
        perm = np.random.permutation(np.arange(entities[k]))
        permutation = dict()
        for i in range(len(perm)):
            permutation[i+1] = perm[i] + 1
        permutations[k] = permutation
    print(permutations.keys())
    return permutations

def readFile(filePath):
  f = open(filePath, "r")
  return f.read()

def writeFileCSV(filePath, content):
    f = open(filePath, "w")
    f.write("text,summary\n")
    for e in content:
        f.write(e[0] + ',' + e[1] + "\n")
    f.close()

def invertMap(map):
    nv_map = {v: k for k, v in map.items()}
    return nv_map

def anonymizeCorpusPermutation(corpus, f, ner):
  processed = ner(corpus)
  res = []
  result = 0
  for entity in processed:
      if entity.ent_type_:
          result += 1
          entity_word = entity.text
          #print(entity.ent_type_)
          replacement = placeholders_map[entity_word]
          permutation = permutations[entity.ent_type_]
          try:
            number_of_placeholder = permutation[numFromPlaceholder(replacement)]
          except:
            print(f"{entity.ent_type_} {replacement} {numFromPlaceholder(replacement)} {entity_word}")
          res.append(inv_placeholders[entity.ent_type_ + "_" + str(number_of_placeholder)])
      else:
          res.append(entity.text)
  write(f, " ".join(res))
  return result

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
    with open("../files/all_ners.txt", "w") as f1:
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
        writeFileJSONAnon(filePath+fileName+"_anonymized_spacy2_"+methodName+".json", together, methodFunc, task)
    else:
        writeFileJSON(filePath+fileName+".json", together)
    return


placeholders_map, max_entities = readPlaceholderMap()
permutations = createPermutationsForEntities(max_entities)
inv_placeholders = invertMap(placeholders_map)
def main():

    path = sys.argv[1]
    if len(sys.argv)>2 and sys.argv[2] == 'anon':
        methodName = sys.argv[3]
        task = sys.argv[4]
        if methodName == 'ner-placeholder':
            method = anonymizeCorpus
        elif methodName == "ner-permutation":
            method = anonymizeCorpusPermutation
        processFile(path, 'train', True, method, methodName, task)
        processFile(path,  'test', True, method, methodName, task)
        processFile(path,   'val', True, method, methodName, task)
        if methodName == 'ner-placeholder':
            with open(f'placeholders_spacy_{task}1.json', 'w') as f:
                f.write(json.dumps(entity_map))
    else:
        processFile(path, 'train', False, None, "", "")
        processFile(path, 'test', False, None, "", "")
        processFile(path, 'val', False, None, "", "")
main()