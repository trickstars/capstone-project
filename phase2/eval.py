import json
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter
from mlxtend.preprocessing import TransactionEncoder

with open('output/evaluate/arm_eval4.json', 'r', encoding='utf-8') as file:
    datasets = json.load(file)
    # data = json.load(file)

# result = []
# for component in datasets:
#     intent = component["intent_label"]
#     if intent != "khác":
#         # entities = list(set([entity["entity_type"] for entity in component["entities"] if entity["entity_type"] != "-1"]))
#         entities = list(set([entity["type_check"] for entity in component["entities"] if entity["type_check"] != "2"]))

#         result.append([intent] + entities)
# result.sort()
# with open('output/evaluate/arm_label.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)

# count = Counter(sublist[0] for sublist in datasets)
# result = {}
# for sublist in datasets:
#     key = sublist[0]  
#     if count[key] >= 4:
#         if key not in result:
#             result[key] = []
#         result[key].append(sublist)
# list_of_lists = list(result.values())
# list_of_lists.sort()
# with open('output/evaluate/arm_eval4.json', 'w', encoding='utf-8') as f:
#     json.dump(list_of_lists, f, ensure_ascii=False, indent=4)

results = []
num = 0.8
for data in datasets:
    encoder = TransactionEncoder()
    encoded_data = encoder.fit(data).transform(data)
    df = pd.DataFrame(encoded_data, columns=encoder.columns_)
    
    frequent_itemsets = apriori(df, min_support=num, use_colnames=True)
    
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=num)
    
    first_elements = [sublist[0] for sublist in data]  
    filtered_rules = rules[rules['antecedents'].apply(
        lambda x: len(x) == 1 and list(x)[0] in first_elements  
    )].copy()
    
    results.append(filtered_rules)

all_results = pd.concat(results, ignore_index=True)

all_results.to_excel(f'arm_eval/4/eval{num}.xlsx', index=False)