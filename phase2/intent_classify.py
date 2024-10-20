import json

with open('old/list_intent.json', 'r', encoding='utf-8') as file:
    intent_list = json.load(file)

from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model_name = 'VoVanPhuc/sup-SimCSE-VietNamese-phobert-base'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# embed sentence using SimCSE
def embed_sentence(sentence, model, tokenizer):
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        embeddings = model(**inputs, return_dict=True).pooler_output
    return embeddings.cpu().numpy()

# find most similar intent
intent_embeddings = np.array([embed_sentence(intent, model, tokenizer) for intent in intent_list]).squeeze(1)

def find_most_similar_intent(input_sentence, intent_embeddings, intent_list):
    input_embedding = embed_sentence(input_sentence, model, tokenizer)
  
    similarities = cosine_similarity(input_embedding, intent_embeddings)
    most_similar_idx = np.argmax(similarities)
    return intent_list[most_similar_idx]

with open(f'output/evaluate/file_0.json', 'r', encoding='utf-8') as f:
  data = json.load(f)

# print(len(data))
#302
for i in range(0,302):
  input_sentence = data[i]['intent_from_mrc'] 
  data[i]['intent_similarity'] = find_most_similar_intent(input_sentence, intent_embeddings, intent_list)

with open(f'output/evaluate/file_0.json', 'w', encoding='utf-8') as f:
  json.dump(data, f, ensure_ascii=False, indent=4)

