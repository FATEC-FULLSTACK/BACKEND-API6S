import os
import json
from dotenv import load_dotenv
from app.database.chroma_database import get_vector_database
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage

load_dotenv()
chroma_db = get_vector_database()

# Cadeia de resumo
summarizer = ChatOpenAI(model="gpt-4o", temperature=0)
summarize_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Resuma o seguinte conteúdo técnico em um parágrafo claro, conciso e objetivo."),
    HumanMessagePromptTemplate.from_template("{content}")
])
summarize_chain = summarize_prompt | summarizer

def retrieve_docs(query: str, n_results: int = 3) -> str:
    results = chroma_db.query(query_texts=query, n_results=n_results)
    if not results or not results.get("documents"):
        return ""
    return "\n".join(results["documents"][0])

async def prepare_context_and_summary(message: str) -> str:
    raw = retrieve_docs(message)
    try:
        summary = (await summarize_chain.ainvoke({"content": raw})).content
        return summary
    except Exception as e:
        return f"Erro ao resumir contexto: {str(e)}"

def format_response(model_name: str, content: str) -> str:
    return f"data: {json.dumps({'model': model_name, 'response': content}, ensure_ascii=False)}\n\n"
