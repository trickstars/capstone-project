import os
from underthesea import ner, sent_tokenize
import json


# input_folder = 'input/faq_split'
# output_folder = 'input/data_label'

# os.makedirs(output_folder, exist_ok=True)

# def process_file(input_file, output_file):
#     with open(input_file, 'r', encoding='utf-8') as file:
#         text = file.read()

#     data = []

#     sentences = sent_tokenize(text)
#     for sen in sentences:
#         sentence = []
#         entities = ner(sen)
#         for entity in entities:
#             sentence.append((entity[0], entity[3]))  
#         data.append(sentence)  

#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)

# for i in range(1, 2):
#     input_file = os.path.join(input_folder, f'faq_{i}.json')
#     output_file = os.path.join(output_folder, f'faq.json')
#     process_file(input_file, output_file)

with open('input/faq_split/faq_1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


for i, text in enumerate(data):
    each = []
    sentences = sent_tokenize(text) 
    for sentence in sentences:
        result = []
        entities = ner(sentence) 
        for entity in entities:
            result.append([entity[0], entity[3]]) 

        each.append(result)  

    # Tạo đường dẫn output nếu chưa có
    output_dir = 'input/data_label/faq'
    os.makedirs(output_dir, exist_ok=True)

    with open(f'{output_dir}/faq_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(each, f, ensure_ascii=False, indent=4)

print("Processing complete.")
