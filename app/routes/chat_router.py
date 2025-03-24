from fastapi import APIRouter, HTTPException
from models.models import ChatRequest
from services.chat import process_chat 
from typing import Any

chat_router = APIRouter()

@chat_router.post("/chat", response_model=dict)
async def chat(request: ChatRequest) -> Any:
    try:
        response = await process_chat(request)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
