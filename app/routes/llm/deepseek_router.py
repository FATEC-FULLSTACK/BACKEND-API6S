from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.models import ChatRequest
from app.services.llm.stream_deepseek import stream_deepseek

router = APIRouter(prefix="/chat/stream")

@router.post("/deepseek")
async def chat_stream_deepseek(request: ChatRequest):
    return StreamingResponse(stream_deepseek(request), media_type="text/event-stream")
