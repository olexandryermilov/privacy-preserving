import sys

import pandas as pd
import csv

def readFile(filePath):
  f = open(filePath, "r")
  return f.read()

def writeFile(filePath, content):
    f = open(filePath, "w")
    f.write("text,summary\n")
    for e in content:
        f.write(e[0] + ',' + e[1] + "\n")
    f.close()

def processFile(filePath, fileName):
    source = readFile(filePath + fileName + '.source').split("\n")
    target = readFile(filePath + fileName + '.target').split("\n")
    together = list(zip(source, target))
    #df = pd.DataFrame(data = together, columns = ["text", "summary"])
    #df.to_csv(fileName + '.csv', index = False,quoting=csv.QUOTE_NONE, quotechar="",  escapechar="\\")
    writeFile(filePath+fileName+".csv", together)
    return

def main():
    path = sys.argv[1]
    processFile(path, 'train')
    processFile(path, 'test')
    processFile(path, 'val')

main()