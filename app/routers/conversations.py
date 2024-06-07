from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List
import os

from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

router = APIRouter()

# Simple in-memory store for conversational history
memory_store: Dict[str, List[str]] = {}

class Message(BaseModel):
    user_id: str
    message: str

# LangChain setup
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="text-davinci-003")
memory = ConversationBufferMemory()

template = PromptTemplate(
    input_variables=["history", "input"],
    template="Your name is Kojo. You are a helpful and witty AI chatbot. Your mission is to answer questions and engage in a fun educational conversation about agentic AI design patterns conversation.\n\nHistory:\n{history}\n\nUser: {input}\nBot:"
)

# Custom transformation function
def transform_fn(inputs):
    history = inputs['history']
    input_message = inputs['input']
    prompt = template.format(history=history, input=input_message)
    return {"prompt": prompt}

class TransformChain:
    def __init__(self, transform_fn):
        self.transform_fn = transform_fn

    def run(self, **inputs):
        return self.transform_fn(inputs)

transform_chain = TransformChain(transform_fn)

class CustomChain:
    def __init__(self, transform_chain, llm):
        self.transform_chain = transform_chain
        self.llm = llm

    def run(self, **inputs):
        transformed = self.transform_chain.run(**inputs)
        response = self.llm(transformed["prompt"])
        return response

chain = CustomChain(transform_chain, llm)

@router.post("/send_message")
def send_message(message: Message):
    user_id = message.user_id
    if user_id not in memory_store:
        memory_store[user_id] = []
    memory_store[user_id].append(f"User: {message.message}")
    
    # Generate a response using LangChain
    response = generate_response(message.message, user_id)
    memory_store[user_id].append(f"Bot: {response}")
    return {"response": response}

def generate_response(user_message: str, user_id: str) -> str:
    conversation_history = "\n".join(memory_store[user_id])
    response = chain.run(history=conversation_history, input=user_message)
    return response.strip()
