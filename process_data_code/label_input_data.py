import json
# from pathlib import Path
# import os.path

# str = Path(__file__).resolve()
# print(type(str))
# print(os.path.dirname(__file__))

input_file = '../examples/intent_for_message/intent_4.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# print(data)

with open('../ontology/intent_entities.json', 'r', encoding='utf-8') as f:
    map = json.load(f)

# print(map)
# index = -1
for component in data:
    # index += 1
    if component['intent'] == "": 
        continue
    key = component['intent']
    new_label = {}
    for entity in map[key]['entities']:
        new_label[entity] = ""
    component['entities'] = new_label

# print(data)
with open(input_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii = False, indent=4)

