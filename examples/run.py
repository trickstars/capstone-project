import os
from transformers import pipeline
import json
# from huggingface_hub import hf_hub_download

# HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

with open('intent_for_message/intent_1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('template.json', 'r', encoding='utf-8') as f:
    question_data = json.load(f)

def get_entity(question, intent):
    words_to_remove = ["nào", "gì", "bao nhiêu"]
    index = question.find("với") 
    entity = question[index + 3 + 1:-1]
    for word in words_to_remove:
        entity = entity.replace(word, "")
    return entity[0:-1]

model_checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\models--nguyenvulebinh--vi-mrc-base"
nlp = pipeline('question-answering', model=model_checkpoint, tokenizer=model_checkpoint)
answer = []
for component in data:
    if component['intent'] == "": 
        continue
    message = "".join(component['message'])
    triple = {}
    triple["message"] = component['message']
    triple["intent"] = component['intent'] 
    for key, value in question_data.items():
        if key == component['intent']:
            question = question_data[key]
            entity = {}
            for q in question:
                QA_input = {'question': q, 'context': message}
                respond = nlp(QA_input)
                entity[get_entity(q,component['intent'])] = respond['answer']
            triple["entities"] = entity       
    answer.append(triple)

with open('answer1.json', 'w', encoding='utf-8') as f:
    json.dump(answer, f, ensure_ascii = False, indent=4)

