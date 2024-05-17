import json

number_of_answer_files = 5

num_of_corrects = 0
num_of_data_points = 0
for i in range(number_of_answer_files):
    file_read = 'answer' + str(i+1) + ".json"
    with open(file_read, 'r', encoding="utf-8") as f:
        answers = json.load(f)
    num_of_data_points += len(answers)
    for answer in answers:
        num_of_corrects += answer["accuracy"]

EM_score = num_of_corrects / num_of_data_points
print(EM_score)