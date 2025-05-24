from typing import AsyncGenerator
from app.models.models import ChatRequest
from app.services.rag_utils import prepare_context_and_summary, format_response
from langchain_google_genai import ChatGoogleGenerativeAI
from app.services.prompts import chat_template

chain = chat_template | ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=1000)

async def stream_gemini(request: ChatRequest) -> AsyncGenerator[str, None]:
    user_message = request.message
    summarized_context = await prepare_context_and_summary(user_message)

    try:
        result = await chain.ainvoke({"question": user_message, "context": summarized_context})
        content = getattr(result, "content", None)
        yield format_response("gemini", content if isinstance(content, str) else str(result))
    except Exception as e:
        yield format_response("gemini", f"ERRO - {str(e)}")
