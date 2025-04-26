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
from app.database.chroma_database import get_vector_database

# Carregar variáveis de ambiente
load_dotenv()


# LEITURA VARIÁVEL AMBIENTE.
openai_api_key=os.getenv('OPENAI_API_KEY')
llama_api_key=os.getenv('LLAMMA_API_KEY')
google_api_key=os.getenv('GOOGLE_API_KEY')
deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')
chroma_db = get_vector_database()

def retrieve_docs(query : str, n_results : int):
    results = chroma_db.query(query_texts=query, n_results=n_results)
    if results == 0:
        print("não foi encontrado nenhum documento semelhante")
    return results


print(
    openai_api_key,llama_api_key,google_api_key,deepseek_api_key
)

# Instanciar modelos
openai = ChatOpenAI(model="gpt-4o", temperature=0, max_completion_tokens=1000)
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=1000)

#Template original
# Criando o template de interação do chatbot
# chat_template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(content=(
#             "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas. "
#             "Sua função é fornecer respostas técnicas e baseadas em evidências sobre a Doença de Alzheimer. "
#             "Responda de forma clara, objetiva e fundamentada em artigos científicos recentes. "
#             "Estruture suas respostas conforme o seguinte formato:\n\n"
#             "1️⃣ **Introdução**: Breve explicação sobre o tema.\n"
#             "2️⃣ **Fisiopatologia**: Explique os mecanismos biológicos envolvidos.\n"
#             "3️⃣ **Diagnóstico**: Métodos clínicos e laboratoriais utilizados.\n"
#             "4️⃣ **Tratamento Atual**: Terapias medicamentosas e não medicamentosas disponíveis.\n"
#             "5️⃣ **Pesquisas Recentes**: Descobertas e tendências em estudos científicos.\n"
#             "6️⃣ **Conclusão**: Resumo e perspectivas futuras.\n\n"
#             "Cite fontes confiáveis sempre que possível e evite especulações sem embasamento clínico."
#         )),
#         HumanMessagePromptTemplate.from_template(
#             'Por favor, gere um relatório detalhado sobre os avanços no tratamento da Doença de Alzheimer em com base na pergunta abaixo \n {question}.'
#         )
#     ]
# )

#Template simplificado
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=(
            "Você é um assistente médico especializado em neurologia e doenças neurodegenerativas."
            "Sua função é fornecer respostas técnicas e baseadas em evidências sobre a Doença de Alzheimer. "
            "Forneça respostas curtas, técnicas e baseadas em evidências, seguindo este formato:\n\n"
            "1️⃣ **Introdução** (1-2 frases)\n"
            "2️⃣ **Fisiopatologia** (mecanismo biológico resumido)\n"
            "3️⃣ **Diagnóstico** (métodos principais de maneira resumida)\n"
            "4️⃣ **Tratamento Atual** (farmacológico e não farmacológico(apenas o principal tratamento)\n"
            "5️⃣ **Pesquisas Recentes** (inclua apenas achados dos últimos 5 anos com relevância clínica comprovada.)\n"
            "6️⃣ **Conclusão** (1 frase)\n\n"
            "**Regras**:\n"
            "- Seja objetivo, evite textos longos.\n"
            "- Cite apenas fontes se solicitado.\n"
            "- Priorize informações práticas e atualizadas."
            "- Caso uma pergunta não tenha relação com Alzheimer, seja empático e responda de forma respeitosa que você não responde pergunta fora do tema."
        )),
        HumanMessagePromptTemplate.from_template(
            'Por favor, gere um relatório detalhado sobre os avanços no tratamento da Doença de Alzheimer em com base na pergunta abaixo \n {question}.\nUse como base esse contexto: {context}'
        )
    ]
)



# Criando as cadeias de processamento para cada LLM
chain_openai = chat_template | openai
chain_gemini = chat_template | gemini

# Função para processar o chat com todas as LLMs
async def process_chat(request: ChatRequest) -> dict:
    user_id = request.user_id
    user_message = request.message

    results = retrieve_docs(query=user_message, n_results=3)
    print(results["documents"][0])

    try:
        # Enviando a mesma pergunta para todas as LLMs
        openai_response = await chain_openai.ainvoke({"question": user_message, "context": results["documents"][0]})
        gemini_response = await chain_gemini.ainvoke({"question": user_message, "context": results["documents"][0]})

        # Organizando a resposta em JSON estruturado
        result = {
            "user_id": user_id,
            "question": user_message,
            "responses": {
                "openai": openai_response.content,
                "gemini": gemini_response.content
            }
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o chat: {e}")