from datasets import load_dataset
import sklearn.metrics

target = load_dataset("imdb")

with open("predict_results_anon.txt", "r") as f:
    predictions = f.readlines()[1:]
    res_anon = []
    for prediction in predictions:
        res_anon.append(int(prediction.split("\t")[1][0]))
    print(sklearn.metrics.f1_score(target["test"]["label"], res_anon))
with open("predict_results_orig.txt", "r") as f:
    predictions = f.readlines()[1:]
    res_orig = []
    for prediction in predictions:
        res_orig.append(int(prediction.split("\t")[1][0]))
    print(sklearn.metrics.f1_score(target["test"]["label"], res_orig))

print(len(res_anon) == len(res_orig))
k1 = 0
k2 = 0

with open("different_answers.txt", "w") as f:
    for i in range(0, len(res_anon)):
        if(res_anon[i] != res_orig[i]):
            if str(res_anon[i]) == str(target["test"].data["label"][i]):
                k1+=1
            else:
                k2+=1
            f.write(f"index {i}, anonymized_answer = {res_anon[i]}, original_answer = {res_orig[i]}, right_answer = {target['test'].data['label'][i]}, text = {target['test'].data['text'][i]}\n") #target["test"].data["text"][i],
print(k1, k2)