import os
import requests
import numpy as np
from dotenv import load_dotenv
from extract_text import extract_text_from_all_pdfs
import tiktoken

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_embedding(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
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

def split_text(text, max_tokens=8192):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk))
    return chunks

directory = "./documents"
documents = extract_text_from_all_pdfs(directory)

embeddings = []
for title, content in documents.items():
    chunks = split_text(content)
    for chunk in chunks:
        embedding = get_embedding(chunk)
        if embedding is not None:
            embeddings.append(embedding)
        else:
            print(f"Failed to get embedding for chunk in document: {title}")

embeddings = np.array(embeddings)

# Save embeddings for later use
np.save("embeddings.npy", embeddings)
