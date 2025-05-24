from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.models.models import ChatRequest
from app.services.chat import process_chat
from app.services.chat_streaming import stream_chat
from typing import Any
from .llm import openai_router, gemini_router, deepseek_router, groq_router, rag_router

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat(request: ChatRequest) -> Any:
    try:
        response = await process_chat(request)
        return {"status": "success", "data": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@chat_router.post("/chat/stream")
async def chat_stream(chat_request: ChatRequest):
    return StreamingResponse(stream_chat(chat_request), media_type="text/event-stream")

chat_router.include_router(openai_router.router)
chat_router.include_router(gemini_router.router)
chat_router.include_router(deepseek_router.router)
chat_router.include_router(groq_router.router)
chat_router.include_router(rag_router.router)
