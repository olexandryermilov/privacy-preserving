import json
import sys
from tqdm import tqdm

def main1():
    jsonpath = sys.argv[1]
    entities = dict()
    with open(jsonpath) as json_file:
        data = json.load(json_file)
        for k in tqdm(data):
            splitted = data[k].split("_")
            entity = " ".join(splitted[0:-1])
            num = int(splitted[-1])
            if entity in entities:
                entities[entity] = max(entities[entity], num)
            else:
                entities[entity] = num
        with open("summarization_records.json", "w") as result_file:
            result_file.write(json.dumps(entities))
def main():
    jsonpath = sys.argv[1]
    predictions_path = sys.argv[2]
    with open(jsonpath) as json_file:
        data = json.load(json_file)
        with open(predictions_path, "r") as predictions_file:
            corpus = predictions_file.read()
            for k in tqdm(sorted(data, key=lambda k: len(data[k]), reverse=True)):
                corpus = corpus.replace(data[k], k)
            with open("fixed_predictions.txt", "w") as new_predictions:
                new_predictions.write(corpus)


main1()
