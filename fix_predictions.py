import json
import sys

def main():
    jsonpath = sys.argv[1]
    predictions_path = sys.argv[2]
    with open(jsonpath) as json_file:
        data = json.load(json_file)
        with open(predictions_path, "r") as predictions_file:
            corpus = predictions_file.read()
            for k in sorted(data, key=lambda k: len(data[k]), reverse=True):
                if data[k] in corpus or data[k] =="PERSON_11":
                    print(f"{data[k]} {k}")
                corpus = corpus.replace(data[k], k)
            with open("fixed_predictions.txt", "w") as new_predictions:
                new_predictions.write(corpus)


main()
