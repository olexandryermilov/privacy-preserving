import sys
import re
from tqdm import tqdm

def main():
    path_sum = sys.argv[1]
    path_tr = sys.argv[2]
    with open(path_sum, "r") as f:
        lines = f.readlines()
        res = 0
        for line in tqdm(lines):
            res += len(re.findall(r'\w+', line))
        print(f"summ: {res/len(lines)}")
    with open(path_tr, "r") as f:
        lines = f.readlines()
        res = 0
        for line in tqdm(lines):
            res += len(re.findall(r'\w+', line))
        print(f"tr: {res/len(lines)}")
main()