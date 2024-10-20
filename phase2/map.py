import json

with open('output/simcse_9d_20/entity_type.json', 'r', encoding='utf-8') as file:
    data = json.load(file) 

with open('output/cluster/simCSE_min20_9d.json', 'r', encoding='utf-8') as file:
    cluster = json.load(file) 

with open('entities_ner_simi.json', 'r', encoding='utf-8') as file:
    ner_file = json.load(file) 


# collect unique entity type
entity_type = []

for key, value in data.items():
    if value not in entity_type: 
        entity_type.append(value)

result = {} 
# Group keys by their entity type
for i in range(len(entity_type)):
    result[entity_type[i]] = []
    for key, value in data.items():
        if value == entity_type[i]:
            result[entity_type[i]].append(key)

with open('output/simcse_9d_20/count.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

entity_dict = {}

for key, value in result.items():
    entity_dict[key] = []
    for entity_key in value:
        entity_dict[key].extend(cluster[entity_key])


with open('output/simcse_9d_20/formated.json', 'w', encoding='utf-8') as f:
    json.dump(entity_dict, f, ensure_ascii=False, indent=4)

#find entity type of string


def get_type(string, entity_dict):
    for key, value in entity_dict.items():
        if string in value:
            return key
    return "-1"
    
for component in ner_file:
    component['entity_type_list'] = []
    if component['entities']:
        for ele in component['entities']:
            en_type = get_type(ele['entity_string'], entity_dict)
            ele['entity_type'] = en_type
            if en_type != "-1" and en_type not in component['entity_type_list']:
                component['entity_type_list'].append(en_type)
            ele['type_check'] = ""

with open('output/simcse_9d_20/entities_ner.json', 'w', encoding='utf-8') as f:
    json.dump(ner_file, f, ensure_ascii=False, indent=4)