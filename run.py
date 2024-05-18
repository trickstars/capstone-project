# import os
from transformers import pipeline
import json
# from huggingface_hub import hf_hub_download

# HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

from infer import tokenize_function, data_collator, extract_answer
from model.mrc_model import MRCQuestionAnswering
from transformers import AutoTokenizer
import nltk
# nltk.download('punkt')

file_index = 1
input_file = 'examples/intent_for_message/intent_'+ str(file_index) +'.json'
output_file = 'answers' + str(file_index) + '.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('ontology/generated_questions.json', 'r', encoding='utf-8') as f:
    question_data = json.load(f)

def get_entity(question, intent):
    words_to_remove = ["nào", "gì", "bao nhiêu", "mấy"]
    index = question.find("với") 
    entity = question[index + 3 + 1:-1]
    for word in words_to_remove:
        entity = entity.replace(word, "")
    return entity[0:-1]

# model_checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\models--nguyenvulebinh--vi-mrc-base"
model_checkpoint = "nguyenvulebinh/vi-mrc-large"
# nlp = pipeline('question-answering', model=model_checkpoint, tokenizer=model_checkpoint)

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = MRCQuestionAnswering.from_pretrained(model_checkpoint)

answer = []
for component in data:
    if component['intent'] == "":
        answer.append(component) 
        continue
    # message = "\n".join(component['message'])
    message = component['message'][0]
    triple = {}
    if ('comment')  in component: 
        triple['comment'] = component['comment']
    triple["message"] = component['message']
    triple["intent"] = component['intent'] 
    for key, value in question_data.items():
        if key == component['intent']:
            question = question_data[key]
            entity = {}
            for q in question:
                QA_input = {'question': q, 'context': message}

                # respond = nlp(QA_input)
                inputs = [tokenize_function(QA_input, tokenizer)]
                inputs_ids = data_collator(inputs, tokenizer)
                outputs = model(**inputs_ids)
                respond = extract_answer(inputs, outputs, tokenizer)

                entity[get_entity(q,component['intent'])] = respond['answer']
                print(respond)
            triple["entities"] = entity 
    # print(triple)      
    answer.append(triple)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(answer, f, ensure_ascii = False, indent=4)

