import os
from transformers import pipeline
import json
# from huggingface_hub import hf_hub_download

# HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

with open('intent_for_message/intent_5.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('template.json', 'r', encoding='utf-8') as f:
    question_data = json.load(f)

model_checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\models--nguyenvulebinh--vi-mrc-base"
nlp = pipeline('question-answering', model=model_checkpoint, tokenizer=model_checkpoint)
answer = {}
for component in data:
    if component['intent'] == "": 
        continue
    message = "".join(component['message'])
    answer[message] = []
    for key, value in question_data.items():
        if key == component['intent']:
            question = question_data[key]
            for q in question:
                QA_input = {'question': q, 'context': message}
                respond = nlp(QA_input)
                result = [q, respond['answer'], respond['score']]
                answer[message].append(result)

with open('answer5.json', 'w', encoding='utf-8') as f:
    json.dump(answer, f, ensure_ascii = False, indent=4)

