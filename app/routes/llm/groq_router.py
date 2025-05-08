from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.models import ChatRequest
from app.services.llm.stream_groq import stream_groq

router = APIRouter(prefix="/chat/stream")

@router.post("/groq")
async def chat_stream_groq(request: ChatRequest):
    return StreamingResponse(stream_groq(request), media_type="text/event-stream")
