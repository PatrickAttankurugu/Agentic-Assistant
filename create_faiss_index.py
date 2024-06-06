import faiss
import numpy as np

# Load embeddings with allow_pickle=True
embeddings = np.load("embeddings.npy", allow_pickle=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # Using L2 (Euclidean) distance
index.add(embeddings)  # Add the document embeddings to the index

# Save the index to a file
faiss.write_index(index, "faiss_index")
