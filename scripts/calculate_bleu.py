import sys
import re

from nltk.translate.bleu_score import corpus_bleu
from nltk.tokenize import word_tokenize

ref = open(sys.argv[1], "r")
cand = open(sys.argv[2], "r")
refs = [[word_tokenize(re.sub(r'[^\w\s]', '', line))] for line in ref.readlines()]
cands = [word_tokenize(re.sub(r'[^\w\s]', '', line)) for line in cand.readlines()]
print(refs[-1])
print(cands[-1])

score = corpus_bleu(refs, cands)
print(score)