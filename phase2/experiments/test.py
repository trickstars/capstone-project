import json

with open('input/faqdata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# result = []
# for component in data:
    # new_data = {}
    # new_data['question_paragraph'] = component['question_paragraph']
    # new_data['intent_from_mrc'] = component['intent_from_mrc']
    # new_data['intent_similarity'] = component['intent_similarity']
    # new_data['intent_label'] = ""
    # new_data['entities'] = component['entities']
    # result.append(new_data)
    

print(len(data))


# with open('entities_ner_simi.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)




