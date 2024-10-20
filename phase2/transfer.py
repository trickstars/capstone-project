import os
import json

folder_path = 'input/data_label/faq'

for i in range(0, 141):
    file_name = f'faq_{i}.json'
    input_path = os.path.join(folder_path, file_name)
    
    if not os.path.exists(input_path):
        continue
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = {}
    for j, sublist in enumerate(data):
        result[j] = []
        for item in sublist:
            result[j].append({
                'wordForm': item[0],
                'nerLabel': item[1]
            })
    
    output_file_name = f'faq{i}.json'
    output_path = os.path.join(folder_path, output_file_name)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

print(f"Chuyển đổi thành công")




# import json

# # Đọc file JSON vào cấu trúc dữ liệu
# with open('data_label/hcmuttintuc/tintuc.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Chuyển đổi định dạng
# result = {}
# for i, sublist in enumerate(data):
#     result[i] = []
#     for item in sublist:
#         result[i].append({
#             'wordForm': item[0],
#             'nerLabel': item[1]
#         })

# # Ghi lại kết quả vào file JSON mới
# with open('data_label/hcmuttintuc/d16.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)

# print("Chuyển đổi thành công!")
