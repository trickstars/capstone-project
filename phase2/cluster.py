import numpy as np
import hdbscan
import json
from sklearn.metrics import silhouette_score

approach = 'simCSE'
dimensions = 60
umap_embeddings = np.load(f'{approach}_{dimensions}d.npy')

with open('uni_entities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('output/score.json', 'r', encoding='utf-8') as f:
    save_score = json.load(f)

existing_min_cluster_sizes = {entry['min_cluster_size'] for entry in save_score}

for min_cluster_size in range(10, 31, 10):  # Ví dụ từ 50 đến 100 với bước nhảy là 10
    # if min_cluster_size not in existing_min_cluster_sizes:
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean')
    labels = clusterer.fit_predict(umap_embeddings)

    cluster_dict = {}
    for text, label in zip(data, labels):
        label = int(label) 
        if label not in cluster_dict:
            cluster_dict[label] = []
        cluster_dict[label].append(text)

    sorted_data = dict(sorted(cluster_dict.items()))

    with open(f'output/cluster/{approach}_min{min_cluster_size}_{dimensions}d.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=4)

    valid_points = labels >= 0
    num_clusters = len(set(labels[valid_points]))
    score = silhouette_score(umap_embeddings[valid_points], labels[valid_points])
    save_score.append({'embed': approach, 'dimensions': dimensions, 'min_cluster_size': min_cluster_size, 'num_cluster': num_clusters, 'score': float(score)})
    
save_score = sorted(save_score, key=lambda x: x['embed'])
with open('output/score.json', 'w', encoding='utf-8') as f:
    json.dump(save_score, f, ensure_ascii=False, indent=4)

# clusterer = hdbscan.HDBSCAN(min_cluster_size=60, metric ='euclidean')
# labels = clusterer.fit_predict(embeddings)

# # Visualize kết quả gom cụm trong không gian 3D
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')

# scatter = ax.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], umap_embeddings[:, 2], c=labels, cmap='viridis', s=50)

# # Add legend for clusters
# legend1 = ax.legend(*scatter.legend_elements(), title="Clusters")
# ax.add_artist(legend1)

# ax.set_title('3D visualization of HDBSCAN clusters using UMAP')
# plt.show()
