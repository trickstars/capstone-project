from transformers import pipeline, AutoTokenizer
import json

with open(f'entities_ner_simi.json', 'r', encoding='utf-8') as f:
  data = json.load(f)

model_checkpoint = "C:\\Users\\Dell\\.cache\\huggingface\\hub\\mrc-large"
nlp = pipeline('question-answering', model=model_checkpoint)
# tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

#5228
for i in range(0, 101):
  context = data[i]['question_paragraph'] 
  intent = data[i]['intent_similarity']
  QA_input = {
    'question': f"Có phải tôi muốn {intent} không? Hãy trả lời có hoặc không",
    'context': context
  }
  res = nlp(QA_input)
  data[i]['intent_verification'] = res['answer']

with open(f'entities_ner_simi.json', 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=4)

