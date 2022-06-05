from datasets import load_dataset
import sklearn.metrics
import sys
from tqdm import tqdm
import json
import re

import spacy
ds = load_dataset("imdb")
source = ds["test"]["text"]
source2 = ds["train"]["text"]
res = 0
for line in tqdm(source):
    res += len(re.findall(r'\w+', line))
for line in tqdm(source2):
    res += len(re.findall(r'\w+', line))
print(f"tr: {res/(len(source) +len(source2))}")