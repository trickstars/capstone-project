import json

# Đọc dữ liệu từ file JSON
with open('../ontology/intent_entities_with_wh.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


output_data = {}

for key, value in data.items():
    # Lấy danh sách entities
    entities = value["entities"]
    
    # Tạo danh sách câu hỏi mới
    questions = [f"{key} với {entity}?" for entity in entities]
    
    # Lưu câu hỏi vào dictionary mới
    output_data[key] = questions

# Ghi dữ liệu mới ra file JSON
with open('../ontology/temp1_gq.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii = False, indent=4)
