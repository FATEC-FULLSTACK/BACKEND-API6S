from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.models import ChatRequest
from app.services.llm.stream_rag import stream_rag

router = APIRouter(prefix="/chat/stream")

@router.post("/rag")
async def chat_stream_rag(request: ChatRequest):
    return StreamingResponse(stream_rag(request), media_type="text/event-stream")
