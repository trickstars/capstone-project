import json

input_file = 'answer5.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

for component in data:
    component["accuracy"] = 0

with open(input_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii = False, indent=4)