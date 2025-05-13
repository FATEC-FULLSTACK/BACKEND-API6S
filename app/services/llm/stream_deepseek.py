from typing import AsyncGenerator
from app.models.models import ChatRequest
from app.services.prompts import chat_template
from app.services.rag_utils import prepare_context_and_summary, format_response
from langchain_deepseek import ChatDeepSeek
from app.services.rag_utils import format_response

chain = chat_template | ChatDeepSeek(model="deepseek-chat", temperature=0, max_tokens=1000)

async def stream_deepseek(request: ChatRequest) -> AsyncGenerator[str, None]:
    user_message = request.message
    summarized_context = await prepare_context_and_summary(user_message)
    
    try:
        result = await chain.ainvoke({"question": user_message, "context": summarized_context})
        content = getattr(result, "content", None)
        yield format_response("deepseek", content if isinstance(content, str) else str(result))
    except Exception as e:
        yield format_response("deepseek", f"ERRO - {str(e)}")
