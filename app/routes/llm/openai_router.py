from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.models import ChatRequest
from app.services.llm.stream_openai import stream_openai

router = APIRouter(prefix="/chat/stream")

@router.post("/openai")
async def chat_stream_openai(request: ChatRequest):
    return StreamingResponse(stream_openai(request), media_type="text/event-stream")
