from typing import AsyncGenerator
from app.models.models import ChatRequest
from app.services.rag_utils import prepare_context_and_summary, format_response
from langchain_openai import ChatOpenAI
from app.services.prompts import chat_template

chain = chat_template | ChatOpenAI(model="gpt-4o", temperature=0, max_completion_tokens=1000)

async def stream_openai(request: ChatRequest) -> AsyncGenerator[str, None]:
    user_message = request.message
    summarized_context = await prepare_context_and_summary(user_message)

    try:
        result = await chain.ainvoke({"question": user_message, "context": summarized_context})
        content = getattr(result, "content", None)
        yield format_response("openai", content if isinstance(content, str) else str(result))
        
    except Exception as e:
        yield format_response("openai", f"ERRO - {str(e)}")
