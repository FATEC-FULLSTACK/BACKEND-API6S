from typing import AsyncGenerator
import json
from app.models.models import ChatRequest
from app.services.rag_utils import prepare_context_and_summary, format_response

async def stream_rag(request: ChatRequest) -> AsyncGenerator[str, None]:
    user_message = request.message
    try:
        summarized_context = await prepare_context_and_summary(user_message)
        yield format_response("rag", summarized_context)
    except Exception as e:
        yield format_response("rag", f"ERRO - {str(e)}")
