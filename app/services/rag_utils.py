import os
import json
from dotenv import load_dotenv
from app.database.chroma_database import get_vector_database
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

load_dotenv()
chroma_db = get_vector_database()

def retrieve_docs(query: str, n_results: int = 3) -> str:
    results = chroma_db.query(query_texts=query, n_results=n_results)
    if not results or not results.get("documents"):
        return ""
    return "\n".join(results["documents"][0])

async def prepare_context_and_summary(message: str) -> str:
    try:
        return retrieve_docs(message)
    except Exception as e:
        return f"Erro ao recuperar contexto: {str(e)}"

def format_response(model_name: str, content: str) -> str:
    return f"data: {json.dumps({'model': model_name, 'response': content}, ensure_ascii=False)}\n\n"
