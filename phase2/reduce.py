import numpy as np
import umap.umap_ as umap

embeddings = np.load('simCSE.npy')

reducer = umap.UMAP(n_neighbors= 15, n_components=60)
umap_embeddings = reducer.fit_transform(embeddings)

np.save('simCSE_60d.npy', umap_embeddings)

print("UMAP embeddings đã được lưu.")
