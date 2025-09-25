from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os

router = APIRouter(prefix="/chat", tags=["chat"])

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ChatRequest(BaseModel):
    query: str
    data: list # Expecting a list of dictionaries (like a pandas DataFrame's records)

@router.post("/")
async def chat_with_data(request: ChatRequest):
    prompt = f"""
    You are a data analysis assistant for the Karnataka Environmental Dashboard.
    Analyze the following data and answer the user's query.

    Data:
    {request.data}

    Query:
    {request.query}
    """
    try:
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}