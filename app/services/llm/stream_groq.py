from typing import AsyncGenerator
from app.models.models import ChatRequest
from app.services.rag_utils import prepare_context_and_summary, format_response
from langchain_groq import ChatGroq
from app.services.prompts import chat_template
import os
from pydantic import SecretStr

groq_api_key = SecretStr(os.getenv("GROQ_API_KEY", ""))

chain = chat_template | ChatGroq(model="llama3-70b-8192", api_key=groq_api_key, temperature=0, max_tokens=1000)

async def stream_groq(request: ChatRequest) -> AsyncGenerator[str, None]:
    user_message = request.message
    summarized_context = await prepare_context_and_summary(user_message)

    try:
        result = await chain.ainvoke({"question": user_message, "context": summarized_context})
        content = getattr(result, "content", None)
        yield format_response("groq", content if isinstance(content, str) else str(result))
    except Exception as e:
        yield format_response("groq", f"ERRO - {str(e)}")
