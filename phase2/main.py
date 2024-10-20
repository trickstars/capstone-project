from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import json

with open('output/fullentities.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\edu-ner"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForTokenClassification.from_pretrained(checkpoint)

id2label = model.config.id2label
label2id = model.config.label2id

# list_entities = []
batch_size = 8

for i in range(81,101):
    with open(f'input/faq_split/faq_{i}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for ticket_id in range(len(data)):
        entities = []
        # tickets_batch = data[ticket_id : (ticket_id + 1) * batch_size]
        # ner_result = ner(ticket)
        inputs = tokenizer(data[ticket_id], max_length=512, truncation=True, return_tensors="pt")
        outputs = model(**inputs)

        words = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
        # print(words)
        predictions = outputs.logits.argmax(2)[0].tolist()

        tmp_entity = ""
        curr_ent = 9

        for id, prediction in enumerate(predictions):
            if prediction in range(4):
                if tmp_entity != "":
                    entities.append(tmp_entity)
                tmp_entity = words[id]
                curr_ent = prediction
            elif prediction == curr_ent + 4:
                if words[id].startswith("##"):
                    tmp_entity += words[id][2:]
                else:
                    tmp_entity += " " + words[id]
            else:
                if tmp_entity != "" and tmp_entity not in entities:
                    entities.append(tmp_entity)
                tmp_entity = ""

        result.append({'sentence': data[ticket_id], 'entities': entities})
        # list_entities.append(entities)

with open('output/fullentities.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

# nlp = pipeline("ner", model=model, tokenizer=tokenizer)
# example = "Liên quan vụ việc CSGT bị tố đánh dân, trúng một cháu nhỏ đang ngủ, đang lan truyền trên mạng xã hội, Đại tá Nguyễn Văn Tảo, Phó Giám đốc Công an tỉnh Tiền Giang vừa có cuộc họp cùng Chỉ huy Công an huyện Châu Thành và một số đơn vị nghiệp vụ cấp tỉnh để chỉ đạo làm rõ thông tin."

# Initialize a list to store the results
# def split_text(text, max_length, tokenizer):
#     """Splits text into chunks within the max token length limit."""
#     tokens = tokenizer.tokenize(text)
#     token_chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
#     text_chunks = [tokenizer.convert_tokens_to_string(chunk) for chunk in token_chunks]
#     return text_chunks

# max_length = 512  # Set max length to the model's limit

# result = []

# for sentence in data:
#     text_chunks = split_text(sentence, max_length - 2, tokenizer)  # Subtract 2 for special tokens [CLS] and [SEP]
    
#     entities = []
#     for chunk in text_chunks:
#         ner_results = nlp(chunk)
        
#         current_entity = []
#         for ner in ner_results:
#             if ner['entity'].startswith('B-'):
#                 if current_entity:
#                     entities.append(' '.join(current_entity))
#                     current_entity = []
#                 current_entity.append(ner['word'])
#             elif ner['entity'].startswith('I-'):
#                 current_entity.append(ner['word'])
        
#         if current_entity and current_entity not in entities:
#             entities.append(' '.join(current_entity))
    
#     result.append({'sentence': sentence, 'entities': entities})


