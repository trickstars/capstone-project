import json

conversation = 0
intent = []
entities = []

for i in range(1,6):
    input_file = 'labeled_inputs/input' + str(i) +'.json'
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for item in data:
        if item['intent'] not in intent:
            intent.append(item["intent"])
        if "entities" in item:
            for entity in item['entities']:
                if entity not in entities:
                    entities.append(entity)
    conversation += len(data)

print(conversation)
print(len(intent))
print(len(entities))
