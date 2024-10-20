from sentence_transformers import SentenceTransformer
import numpy as np
import hdbscan
import json
from pyvi.ViTokenizer import tokenize

with open('uni_entities.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)

# model = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
# sentences = [tokenize(sentence) for sentence in data]
# embeddings = model.encode(sentences)

model = SentenceTransformer('keepitreal/vietnamese-sbert')
embeddings = model.encode(data)

# Lưu kết quả embed vào file numpy
np.save('sbert.npy', embeddings)

# # Lưu danh sách các câu và embedding vào file JSON để có thể kết hợp với cụm sau này
# with open('output/data_with_embeddings.json', 'w', encoding='utf-8') as f:
#     json.dump({'data': data, 'embeddings': embeddings.tolist()}, f, ensure_ascii=False, indent=4)

print("Embeddings và dữ liệu đã được lưu.")

# data_embeddings = model.encode(data)
# print(np.array(data_embeddings).shape)

# clustering_model = hdbscan.HDBSCAN(min_cluster_size=2 ,metric='euclidean')
# clustering_model.fit(corpus_embeddings)
# print(clustering_model.labels_)

# num_clusters = 3

# clustering_model = KMeans(n_clusters=num_clusters)
# clustering_model.fit(corpus_embeddings)
# cluster_assignment = clustering_model.labels_
# print(cluster_assignment)