import json

with open('faqdata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


conversation = []
new_data = []

for i in range(len(data) - 1):
    if ("ticket closed" not in data[i]['MESSAGE']) and ("Solved" not in data[i]['MESSAGE']) and ("ticket opened" not in data[i]['MESSAGE']) and  ("category" not in data[i]['MESSAGE']) and ("status" not in data[i]['MESSAGE']) and ("priority" not in data[i]['MESSAGE']) and ("support level" not in data[i]['MESSAGE']):
        string = data[i]['MESSAGE'].replace("&gt", "").replace("&lt", "").replace("li&gt", "").replace("i&gt", "").replace("b&gt", "").strip()
        if string != "":
            new_data.append(string)
    if (data[i]["ticket_tieude"] != data[i + 1]["ticket_tieude"]):
        conversation.append(new_data)
        new_data = []
        
tail = data[len(data)-1]['MESSAGE']
if ("ticket closed" not in tail) and ("Solved" not in tail) and ("ticket opened" not in tail) and  ("category" not in tail) and ("status" not in tail) and ("priority" not in tail) and ("support level" not in data[i]['MESSAGE']):
    tail = tail.replace("&gt", "").replace("&lt", "").replace("li&gt", "").replace("i&gt", "").replace("b&gt", "").strip()
    if tail != "":
        conversation.append(tail) 

# data = []
# for sublist in conversation:
#     joined_string = ''.join(sublist)
#     data.append(joined_string)

# for item in conversation:
#     for i in range(len(item)):
#         item[i] = item[i].replace("&lt", "").replace("li&gt", "").replace("i&gt", "").replace("b&gt", "").strip()

# output = []

# for sublist in conversation:
#     joined_string = "".join(sublist)
#     output.append(joined_string)

# item = [string for string in item if string.strip()]

# string = data[i]['MESSAGE'].replace("&lt;", "").replace("li&gt;", "").replace("i&gt", "").replace("b&gt;", "")

with open('output1.json', 'w', encoding='utf-8') as f:
    json.dump(conversation, f, ensure_ascii=False, indent=4)
