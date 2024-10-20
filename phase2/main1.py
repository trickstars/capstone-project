from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
import json

checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\edu-ner"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForTokenClassification.from_pretrained(checkpoint)

def clean_entity_string(entity):
    """Hàm loại bỏ dấu cách thừa giữa các ký tự đặc biệt"""
    return entity.replace(" . ", ".").replace(" , ", ",").replace(" / ", "/").replace(" - ", "-").replace(" ( ", "(").replace(" ) ", ")")

for i in range(10, 11):
    # Load file input
    with open(f'output/random_data{i}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = []
    for ticket_id in range(len(data)):
        sentence = data[ticket_id]
        
        # Tokenize và lấy offset_mapping để theo dõi vị trí token trong câu gốc
        inputs = tokenizer(sentence, max_length=512, truncation=True, return_tensors="pt", return_offsets_mapping=True)
        
        # Tách offset_mapping ra khỏi inputs để không đưa vào mô hình
        offset_mapping = inputs.pop("offset_mapping")
        
        outputs = model(**inputs)

        # Lấy token và dự đoán
        words = tokenizer.convert_ids_to_tokens(inputs.input_ids[0])
        predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()
        offsets = offset_mapping[0].tolist()  # Lấy vị trí start và end của từng token trong câu

        entities = []
        tmp_entity = ""
        entity_start = 0
        curr_ent = 9  # Default giá trị không liên quan đến bất kỳ entity tag nào

        for idx, prediction in enumerate(predictions):
            start_pos, end_pos = offsets[idx]
            if prediction in range(4):  # B-tag
                if tmp_entity != "":
                    entities.append({
                        'entity_string': clean_entity_string(tmp_entity),
                        'entity_start_position': entity_start,
                        'entity_end_position': offsets[idx-1][1]
                    })
                tmp_entity = words[idx].replace("##", "")
                entity_start = start_pos  # Save the start pos of entity
                curr_ent = prediction
            elif prediction == curr_ent + 4:  # I-tag
                if words[idx].startswith("##"):
                    tmp_entity += words[idx][2:]
                else:
                    tmp_entity += " " + words[idx]
            else:
                if tmp_entity != "":
                    entities.append({
                        'entity_string': clean_entity_string(tmp_entity),
                        'entity_start_position': entity_start,
                        'entity_end_position': offsets[idx-1][1]
                    })
                tmp_entity = ""

        result.append({
            'question_paragraph': sentence,
            'entities': entities
        })

    with open('entities.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
