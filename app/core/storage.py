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
