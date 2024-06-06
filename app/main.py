from fastapi import FastAPI, Body
from pydantic import BaseModel
import numpy as np
from app.core.storage import search, get_embedding

app = FastAPI()

class QueryModel(BaseModel):
    query: str

@app.post("/search")
def search_documents(query_model: QueryModel):
    query_embedding = get_embedding(query_model.query)
    distances, indices = search(np.array(query_embedding))
    return {"distances": distances.tolist(), "indices": indices.tolist()}
