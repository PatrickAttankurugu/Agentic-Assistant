import faiss
import numpy as np
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FAISS_INDEX_NAME = os.getenv("FAISS_INDEX_NAME", "faiss_index")

# Load the FAISS index
index = faiss.read_index(FAISS_INDEX_NAME)

def search(query_embedding, k=5):
    distances, indices = index.search(np.array([query_embedding]), k)
    return distances, indices

def get_embedding(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        if 'data' in response_json:
            return response_json['data'][0]['embedding']
        else:
            print("Key 'data' not found in the response:", response_json)
            return None
    else:
        print("Failed to get embedding:", response.status_code, response.text)
        return None

def rank_results(distances, indices):
    # Combine distances and indices into a list of tuples
    results = list(zip(distances[0], indices[0]))
    # Sort results by distance (lower distance indicates higher relevance)
    ranked_results = sorted(results, key=lambda x: x[0])
    return ranked_results

def search_and_rank(query, k=5):
    query_embedding = get_embedding(query)
    if query_embedding is not None:
        distances, indices = search(query_embedding, k)
        ranked_results = rank_results(distances, indices)
        return ranked_results
    else:
        return []

# Example usage
if __name__ == "__main__":
    query = "Explain the benefits of agentic AI design patterns"
    ranked_results = search_and_rank(query, k=5)
    print("Ranked Results:", ranked_results)
