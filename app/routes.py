from fastapi import APIRouter, HTTPException
from app.models import ChatRequest
from app.services.chat import process_chat

chat_router = APIRouter()

@chat_router.post("/chat")
def chat(request: ChatRequest):
    try:
        response = process_chat(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
