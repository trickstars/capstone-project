# import os
from transformers import pipeline
import json
# from huggingface_hub import hf_hub_download

# HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")

from infer import tokenize_function, data_collator, extract_answer
from model.mrc_model import MRCQuestionAnswering
# from transformers import AutoTokenizer
# import nltk
# nltk.download('punkt')


from transformers import AutoTokenizer, RobertaForQuestionAnswering
import torch

# Tải tokenizer và mô hình


file_index = 1
temp = 1
# input_file = 'examples/intent_for_message/intent_'+ str(file_index) +'.json'
input_file = 'labeled_inputs/input'+ str(file_index) +'.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_entity(question, intent):
    words_to_remove = ["nào", "gì", "bao nhiêu", "mấy"]
    index = question.find("với") 
    entity = question[index + 3 + 1:-1]
    for word in words_to_remove:
        entity = entity.replace(word, "")
    return entity[0:-1]

def get_entity2(question):
    words_to_remove = ["nào", "gì", "bao nhiêu", "mấy"]
    # index = question.find("với") 
    # entity = question[index + 3 + 1:-1]
    for word in words_to_remove:
        question = question.replace(word, "")
    return question[0:-2]

# model_checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\models--nguyenvulebinh--vi-mrc-base"
# model_checkpoint = "nguyenvulebinh/vi-mrc-large"
model_checkpoint = "duyduong9htv/phobert-qa-finetuned-viet-qa"
model_use = "phobert-base"
# nlp = pipeline('question-answering', model=model_checkpoint, tokenizer=model_checkpoint)

# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
# model = MRCQuestionAnswering.from_pretrained(model_checkpoint)

# pt_bin_file = "C:\\Users\\Khoe\\.cache\huggingface\\hub\\models--duyduong9htv--phobert-qa-finetuned-viet-qa\\snapshots\\ae91f0842e02a14a91e3b32f4e6985e205e24d06\\pytorch_model.bin"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = RobertaForQuestionAnswering.from_pretrained(model_checkpoint)

answer = []
def ques_temp(stategy):
    questions = None
    if (stategy == 1):
        with open('ontology/temp1_gq.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    elif (stategy == 2):
        with open('ontology/temp2.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    elif (stategy == 3):
        with open('ontology/temp3.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    return questions

def run_with_temp(temp_stategy):
    question_data = ques_temp(temp_stategy)
    print(question_data)
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
                    inputs = tokenizer(QA_input['question'], QA_input['context'], return_tensors="pt", truncation=True)

                    # Dự đoán câu trả lời
                    with torch.no_grad():
                        outputs = model(**inputs)
                        start_logits = outputs.start_logits
                        end_logits = outputs.end_logits

                    # Xác định vị trí bắt đầu và kết thúc của câu trả lời
                    start_index = torch.argmax(start_logits)
                    end_index = torch.argmax(end_logits)

                    # Chuyển đổi các chỉ số thành câu trả lời
                    answer_tokens = inputs.input_ids[0][start_index:end_index+1]
                    rep = tokenizer.decode(answer_tokens, skip_special_tokens=True)
                    respond = {'answer': rep, 'start': start_index, 'end': end_index}

                    # print(f"Câu trả lời: {respond}")


                    # respond = nlp(QA_input)
                    # inputs = [tokenize_function(QA_input, tokenizer)]
                    # if(not inputs[0]['valid']):
                    #     print("Here it is")
                    # inputs_ids = data_collator(inputs, tokenizer)
                    # outputs = model(**inputs_ids)
                    # respond = extract_answer(inputs, outputs, tokenizer)
                    # if(respond['score_start'] < 0.8 or respond['score_end'] < 0.8):
                    #     respond['answer'] = ''
                    if(temp_stategy == 1):
                        entity[get_entity(q,component['intent'])] = respond['answer']
                    elif(temp_stategy == 2):
                        entity[q] = respond['answer']
                    elif(temp_stategy == 3):
                        entity[get_entity2(q)] = respond['answer']

                    print(respond)
                triple["entities"] = entity 
        # print(triple)      
        answer.append(triple)

    output_file = model_use + '/temp' + str(temp_stategy) + '_answers/answers' + str(file_index) + '.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(answer, f, ensure_ascii = False, indent=4)

#run
run_with_temp(temp)