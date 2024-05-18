import json
import shutil

# read json file
with open('output1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#copy data and add key itnent 
new_data = []
for item in data:
    new_item = {"intent": "", "message": item}
    new_data.append(new_item)

# write to new file
with open('intent_labeled.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)
