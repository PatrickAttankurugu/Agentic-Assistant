from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()

@router.get("/greet")
def greet_user():
    return {"message": "Hello! How can I assist you today?"}

@router.get("/help")
def help():
    return {
        "message": "You can ask me questions about the documents. Try asking about specific topics or keywords."
    }

@router.get("/faq")
def faq():
    faqs = {
        "What is this chatbot?": "This is a chatbot designed to help you with information retrieval.",
        "How do I use this chatbot?": "Simply type in a query, and I will search for relevant information in the documents."
    }
    return faqs

class QueryModel(BaseModel):
    query: str

@router.post("/query")
def query_documents(query_model: QueryModel):
    # Placeholder for query handling logic
    return {"message": f"Searching for: {query_model.query}"}

class FeedbackModel(BaseModel):
    feedback: str

@router.post("/feedback")
def user_feedback(feedback_model: FeedbackModel):
    # Placeholder for storing user feedback
    return {"message": "Thank you for your feedback!"}
