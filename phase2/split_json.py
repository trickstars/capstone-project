import json

def split_json(input_file, output_prefix, num_parts):
    with open(input_file, 'r', encoding = 'utf-8') as f:
        data = json.load(f)

    total_records = len(data)
    records_per_part = total_records // num_parts

    for i in range(num_parts):
        start_index = i * records_per_part
        end_index = start_index + records_per_part if i < num_parts - 1 else total_records
        part_data = data[start_index:end_index]
        output_file = f"{output_prefix}_{i+1}.json"
        with open(output_file, 'w', encoding = 'utf-8') as f:
            json.dump(part_data, f, ensure_ascii=False, indent=4)

input_file = "output/simcse_9d_20/entities_ner.json"
output_prefix = "output/evaluate/file"
num_parts = 50

split_json(input_file, output_prefix, num_parts)
