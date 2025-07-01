import os
import asyncio
from dotenv import load_dotenv
from pydantic import SecretStr
from fastapi import HTTPException
from typing import Dict
from langchain_openai import ChatOpenAI
from app.models.models import ChatRequest
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_deepseek import ChatDeepSeek
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.database.chroma_database import get_vector_database

# Carregar variáveis de ambiente
load_dotenv()


# LEITURA VARIÁVEL AMBIENTE.
openai_api_key=os.getenv('OPENAI_API_KEY')
llama_api_key=os.getenv('LLAMMA_API_KEY')
google_api_key=os.getenv('GOOGLE_API_KEY')
deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')
groq_api_key = SecretStr(os.getenv('GROQ_API_KEY') or "") # implementado ultima revisão
chroma_db = get_vector_database()

def retrieve_docs(query : str, n_results : int):
    results = chroma_db.query(query_texts=query, n_results=n_results)
    if results == 0:
        print("não foi encontrado nenhum documento semelhante")
    return results

# Instanciar modelos
openai = ChatOpenAI(model="gpt-4o", temperature=0, max_completion_tokens=1000)
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=1000)
deepseek = ChatDeepSeek(model="deepseek-chat", temperature=0, max_tokens=1000)
groq = ChatGroq(model="llama3-70b-8192", api_key=groq_api_key, temperature=0, max_tokens=1000)

#Template simplificado
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(
            "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas."
            "Sua função é fornecer respostas técnicas e baseadas em evidências sobre a Doença de Alzheimer. "
            "Forneça respostas curtas, técnicas e baseadas em evidências\n\n"
            "**Regras**:\n"
            "- Seja objetivo, evite textos longos.\n"
            "- Cite apenas fontes se solicitado.\n"
            "- Priorize informações práticas e atualizadas.\n"
            "- Se for fornecido um contexto use ele como base na resposta.\n"
            "- Caso uma pergunta não tenha relação com Alzheimer, seja empático e responda de forma respeitosa que você não responde pergunta fora do tema."
        )),
        HumanMessagePromptTemplate.from_template(
            'Por favor, fale sobre a Doença de Alzheimer em com base na pergunta abaixo \n {question}.\n\ncontexto: {context}'
        )
    ]
)

chat_template_sem_rag = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(
            "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas."
            "Sua função é fornecer respostas técnicas e baseadas em evidências sobre a Doença de Alzheimer. "
            "Forneça respostas curtas, técnicas e baseadas em evidências\n\n"
            "**Regras**:\n"
            "- Seja objetivo, evite textos longos.\n"
            "- Cite apenas fontes se solicitado.\n"
            "- Priorize informações práticas e atualizadas.\n"
            "- Se for fornecido um contexto use ele como base na resposta.\n"
            "- Caso uma pergunta não tenha relação com Alzheimer, seja empático e responda de forma respeitosa que você não responde pergunta fora do tema."
        )),
        HumanMessagePromptTemplate.from_template(
            'Por favor, fale sobre a Doença de Alzheimer em com base na pergunta abaixo \n {question}.'
        )
    ]
)



# Criando as cadeias de processamento para cada LLM
chain_openai_com_rag = chat_template | openai
chain_gemini_com_rag = chat_template | gemini
chain_deepseek_com_rag = chat_template | deepseek
chain_groq_com_rag = chat_template | groq

chain_openai_sem_rag = chat_template_sem_rag | openai
chain_gemini_sem_rag = chat_template_sem_rag | gemini
chain_deepseek_sem_rag = chat_template_sem_rag | deepseek
chain_groq_sem_rag = chat_template_sem_rag | groq 
    
async def Gerar_relatorio_gemini(request: str) -> dict:
    
    results = retrieve_docs(query=request, n_results=3)
    try:
        results = retrieve_docs(query=request, n_results=3)
        # Enviando a mesma pergunta para todas as LLMs
        responses = await asyncio.gather(
            chain_gemini_com_rag.ainvoke({"question": request, "context": results["documents"][0]}),
            chain_gemini_sem_rag.ainvoke({"question": request}),
            return_exceptions=True
        )

        gemini_com_rag, gemini_sem_rag  = responses

        # Organizando a resposta em JSON estruturado
        result = {
            "pergunta": request,
            "resposta_com_rag": gemini_com_rag.content,
            "resposta_sem_rag": gemini_sem_rag.content
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o chat: {e}")

async def Gerar_relatorio_deepseek(request) -> dict:
    results = retrieve_docs(query=request, n_results=3)
    try:
        # Enviando a mesma pergunta para todas as LLMs
        responses = await asyncio.gather(
            chain_deepseek_com_rag.ainvoke({"question": request, "context": results["documents"][0]}),
            chain_deepseek_sem_rag.ainvoke({"question": request}),
            return_exceptions=True
        )

        deepseek_com_rag, deepseek_sem_rag = responses

        resultado = {
            "pergunta": request,
            "resposta_com_rag": deepseek_com_rag.content,
            "resposta_sem_rag": deepseek_sem_rag.content
        }
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o chat: {e}")


async def Gerar_relatorio_openai(request) -> dict:
    
    results = retrieve_docs(query=request, n_results=3)
    try:
        # Enviando a mesma pergunta para todas as LLMs
        responses = await asyncio.gather(
            chain_openai_com_rag.ainvoke({"question": request, "context": results["documents"][0]}),
            chain_openai_sem_rag.ainvoke({"question": request}),
            return_exceptions=True
        )

        openai_com_rag, openai_sem_rag = responses

        # Organizando a resposta em JSON estruturado
        result = {
            "pergunta": request,
            "resposta_com_rag": openai_com_rag.content, 
            "resposta_sem_rag": openai_sem_rag.content
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o chat: {e}")
    


async def Gerar_relatorio_groq(request) -> dict:
    
    results = retrieve_docs(query=request, n_results=3)
    try:
        # Enviando a mesma pergunta para todas as LLMs
        responses = await asyncio.gather(
            chain_groq_com_rag.ainvoke({"question": request, "context": results["documents"][0]}),
            chain_groq_sem_rag.ainvoke({"question": request}),
            return_exceptions=True
        )

        groq_com_rag, groq_sem_rag = responses

        # Organizando a resposta em JSON estruturado
        result = {
            "pergunta": request,
            "resposta_com_rag": groq_com_rag.content, 
            "resposta_sem_rag": groq_sem_rag.content
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o chat: {e}")
    