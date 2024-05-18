import json

number_of_answer_files = 1

# num_of_corrects = 0
# num_of_data_points = 0

tp = 0
num_ad = 0
num_a = 0

for i in range(number_of_answer_files):
    file_in = 'labeled_inputs/input' + str(i+1) + '.json'
    file_out = 'answers' + str(i+1) + ".json"

    with open(file_out, 'r', encoding="utf-8") as f:
        answers = json.load(f)

    with open(file_in, 'r', encoding="utf-8") as f:
        inputs = json.load(f)

    print(len(inputs) == len(answers))
    for j in range(len(inputs)):
        if(inputs[j]['intent'] == ""):
            continue
        arg_glb = inputs[j]['entities']
        arg_det = answers[j]['entities']
        for key,values in arg_glb.items():
            if arg_glb[key] != '':
                num_a += 1
            if arg_det[key] != '':
                num_ad += 1
            if arg_glb[key] != '' and arg_glb[key] == arg_det[key]:
                print(arg_det[key], arg_glb[key])
                tp += 1

# EM_score = num_of_corrects / num_of_data_points
# print(EM_score)

print(tp, num_a, num_ad)

prec = tp / num_ad
rec = tp / num_a
f1 = 2* (prec * rec) / (prec + rec)

print("Precision: ", prec)
print("Recall: ", rec)
print("F1: ", f1)