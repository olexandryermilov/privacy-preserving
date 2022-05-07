import json
import sys
from tqdm import tqdm

def main():
    jsonpath = sys.argv[1]
    predictions_path = sys.argv[2]
    with open(jsonpath) as json_file:
        data = json.load(json_file)
        with open(predictions_path, "r") as predictions_file:
            corpus = predictions_file.read()
            for k in tqdm(sorted(data, key=lambda k: len(data[k]), reverse=True)):
                corpus = corpus.replace(data[k], k)
            with open("../fixed_predictions.txt", "w") as new_predictions:
                new_predictions.write(corpus)


main()
