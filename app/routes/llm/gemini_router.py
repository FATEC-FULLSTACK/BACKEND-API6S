from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.models import ChatRequest
from app.services.llm.stream_gemini import stream_gemini

router = APIRouter(prefix="/chat/stream")

@router.post("/gemini")
async def chat_stream_gemini(request: ChatRequest):
    return StreamingResponse(stream_gemini(request), media_type="text/event-stream")
