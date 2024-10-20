import json

# with open('output/entities1.json', 'r', encoding='utf-8') as file1:
#     data1 = json.load(file1)

# with open('output/entities2.json', 'r', encoding='utf-8') as file2:
#     data2 = json.load(file2)

# result = []

# for component in data1:
#     for entity in component['entities']:
#         if entity and entity not in result:
#             result.append(entity)

# for component in data2:
#     for entity in component['entities']:
#         if entity and entity not in result:
#             result.append(entity)

# result.sort()

# with open('output/unique_entities.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)



with open(f'output/score.json', 'r', encoding='utf-8') as file:
    data = json.load(file)    

save_score = sorted(data, key=lambda x: x['score'])

# result = []

# for component in data:
#     for entity in component['entities']:
#         if entity['entity_string'] not in result:
#             result.append(entity['entity_string'])

with open('output/sorted_score.json', 'w', encoding='utf-8') as f:
    json.dump(save_score, f, ensure_ascii=False, indent=4)


