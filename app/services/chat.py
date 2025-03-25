import os
from dotenv import load_dotenv
from fastapi import HTTPException
from typing import Dict
from langchain_openai import ChatOpenAI
from app.models.models import ChatRequest
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Carregar variáveis de ambiente
load_dotenv()


# LEITURA VARIÁVEL AMBIENTE.
openai_api_key=os.getenv('OPENAI_API_KEY')
llama_api_key=os.getenv('LLAMMA_API_KEY')
google_api_key=os.getenv('GOOGLE_API_KEY')
deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')

print(
    openai_api_key,llama_api_key,google_api_key,deepseek_api_key
)

# Instanciar modelos
openai = ChatOpenAI(model="gpt-4o", temperature=0, max_completion_tokens=500)
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=500)
#llama = OllamaLLM(model="llama3", temperature=0)
#deepseek = ChatDeepSeek(model="deepseek-chat", temperature=0, max_tokens=500)

# Criando o template de interação do chatbot
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(
            "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas. "
            "Sua função é fornecer respostas técnicas e baseadas em evidências sobre a Doença de Alzheimer. "
            "Responda de forma clara, objetiva e fundamentada em artigos científicos recentes. "
            "Estruture suas respostas conforme o seguinte formato:\n\n"
            "1️⃣ **Introdução**: Breve explicação sobre o tema.\n"
            "2️⃣ **Fisiopatologia**: Explique os mecanismos biológicos envolvidos.\n"
            "3️⃣ **Diagnóstico**: Métodos clínicos e laboratoriais utilizados.\n"
            "4️⃣ **Tratamento Atual**: Terapias medicamentosas e não medicamentosas disponíveis.\n"
            "5️⃣ **Pesquisas Recentes**: Descobertas e tendências em estudos científicos.\n"
            "6️⃣ **Conclusão**: Resumo e perspectivas futuras.\n\n"
            "Cite fontes confiáveis sempre que possível e evite especulações sem embasamento clínico."
        )),
        HumanMessagePromptTemplate.from_template(
            'Por favor, gere um relatório detalhado sobre os avanços no tratamento da Doença de Alzheimer em com base na pergunta abaixo \n {question}.'
        )
    ]
)

# Criando as cadeias de processamento para cada LLM
chain_openai = chat_template | openai
chain_gemini = chat_template | gemini
#chain_llama = chat_template | llama
#chain_deepseek = chat_template | deepseek


# Função para processar o chat com todas as LLMs
async def process_chat(request: ChatRequest) -> dict:
    user_id = request.user_id
    user_message = request.message

    try:
        # Enviando a mesma pergunta para todas as LLMs
        openai_response = await chain_openai.ainvoke({"question": user_message})
        gemini_response = await chain_gemini.ainvoke({"question": user_message})
        #llama_response = await chain_llama.invoke({"question": user_message})
        #deepseek_response = await chain_deepseek.invoke({"question": user_message})

        # Organizando a resposta em JSON estruturado
        result = {
            "user_id": user_id,
            "question": user_message,
            "responses": {
                "openai": openai_response.content,
                "gemini": gemini_response.content
                #"llama": llama_response.content,
                #"deepseek": deepseek_response.content
            }
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o chat: {e}")