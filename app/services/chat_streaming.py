import os
import json
from dotenv import load_dotenv
from typing import AsyncGenerator
from asyncio import create_task, as_completed
from pydantic import SecretStr
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from app.models.models import ChatRequest
from app.database.chroma_database import get_vector_database

# Carregar variáveis de ambiente
load_dotenv()

# Leitura de variáveis de ambiente
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = SecretStr(os.getenv('GROQ_API_KEY') or "")

# Banco vetorial
chroma_db = get_vector_database()

# Função de recuperação de contexto
def retrieve_docs(query: str, n_results: int = 3) -> str:
    results = chroma_db.query(query_texts=query, n_results=n_results)
    if not results or not results.get("documents"):
        print("Nenhum documento semelhante encontrado")
        return ""
    return "\n".join(results["documents"][0])

# Template padrão de prompt
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas."
        "Sua função é fornecer respostas técnicas e baseadas em evidências sobre a Doença de Alzheimer."
        "\n\n**Regras**:\n"
        "- Seja objetivo, evite textos longos.\n"
        "- Cite apenas fontes se solicitado.\n"
        "- Priorize informações práticas e atualizadas.\n"
        "- Use o contexto fornecido como base.\n"
        "- Caso a pergunta não seja sobre Alzheimer, responda de forma empática que não pode responder."
    )),
    HumanMessagePromptTemplate.from_template(
        'Por favor, fale sobre a Doença de Alzheimer com base na pergunta abaixo:\n{question}\n\ncontexto: {context}'
    )
])

# Cadeia de resumo para o RAG
summarizer = ChatOpenAI(model="gpt-4o", temperature=0)
summarize_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Resuma o seguinte conteúdo técnico em um parágrafo claro, conciso e objetivo."),
    HumanMessagePromptTemplate.from_template("{content}")
])
summarize_chain = summarize_prompt | summarizer

# Cadeias para cada modelo
chain_openai = chat_template | ChatOpenAI(model="gpt-4o", temperature=0, max_completion_tokens=1000)
chain_gemini = chat_template | ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=1000)
chain_deepseek = chat_template | ChatDeepSeek(model="deepseek-chat", temperature=0, max_tokens=1000)
chain_groq = chat_template | ChatGroq(model="llama3-70b-8192", api_key=groq_api_key, temperature=0, max_tokens=1000)

# Função de streaming
async def stream_chat(request: ChatRequest) -> AsyncGenerator[str, None]:
    user_id = request.user_id
    user_message = request.message

    # Recuperar contexto
    raw_context = retrieve_docs(user_message)

    # Resumir contexto
    try:
        summarized_context = (await summarize_chain.ainvoke({"content": raw_context})).content
    except Exception as e:
        summarized_context = f"Erro ao resumir contexto: {str(e)}"

    # Primeiro enviar o RAG
    yield f"data: {json.dumps({'model': 'rag', 'response': summarized_context}, ensure_ascii=False)}\n\n"

    # Configurar as cadeias de LLMs
    chains = {
        "openai": chain_openai,
        "gemini": chain_gemini,
        "deepseek": chain_deepseek,
        "groq": chain_groq,
    }

    async def invoke_and_yield(name, chain):
        try:
            response = await chain.ainvoke({"question": user_message, "context": summarized_context})
            content = response.content
        except Exception as e:
            content = f"ERRO - {str(e)}"

        return f"data: {json.dumps({'model': name, 'response': content}, ensure_ascii=False)}\n\n"

    # Disparar todas as LLMs em paralelo
    tasks = [create_task(invoke_and_yield(name, chain)) for name, chain in chains.items()]
    for coro in as_completed(tasks):
        yield await coro
