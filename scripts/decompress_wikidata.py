import json
import sys

from tqdm import tqdm
def read_file(file_path):
    with open(file_path, "r") as file:
        return file.readlines()

result = dict()
i = 0
for line in tqdm(read_file(sys.argv[1])):
    js = json.loads(line)
    if js['neClass'] in result.keys():
        result[js['neClass']] = result[js['neClass']] + [js['norm_name']]
    else:
        result[js['neClass']] = [js['norm_name']]
    i += 1
    if i % 10000 == 0:
        with open(f'named_entities_{i}.json', 'a') as f:
            f.write(json.dumps(result))
