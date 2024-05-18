import json

# Đọc dữ liệu từ file JSON
with open('intent_entities.json', 'r', encoding='utf-8') as f:
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
with open('template.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii = False, indent=4)
