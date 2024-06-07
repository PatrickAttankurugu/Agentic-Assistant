from fastapi import FastAPI, Body
from pydantic import BaseModel
import numpy as np
from app.core.storage import search_and_rank
from app.routers import endpoints, conversations

app = FastAPI()

class QueryModel(BaseModel):
    query: str

@app.post("/search")
def search_documents(query_model: QueryModel):
    ranked_results = search_and_rank(query_model.query)
    return {"results": ranked_results}

app.include_router(endpoints.router)
app.include_router(conversations.router)
