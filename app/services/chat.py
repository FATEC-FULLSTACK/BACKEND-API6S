from app.models import ChatRequest
from langchain_core.messages import HumanMessage, AIMessage
from app.services.agent import get_agent_executor

# Armazenamento em memória para o histórico de conversas
chat_histories = {}

def process_chat(request: ChatRequest) -> dict:
    user_id = request.user_id
    user_message = request.message

    # Inicializa o histórico se não existir
    if user_id not in chat_histories:
        chat_histories[user_id] = []
    
    # Adiciona a mensagem do usuário ao histórico
    chat_histories[user_id].append(HumanMessage(user_message))
    
    executor = get_agent_executor()
    
    try:
        # Invoca o executor do agente com a mensagem e o histórico atual
        result = executor.invoke({"input": user_message, "chat_history": chat_histories[user_id]})
        ai_message = result["output"]
        
        # Adiciona a resposta do agente ao histórico
        chat_histories[user_id].append(AIMessage(ai_message))
        
        return {"reply": ai_message}
    except Exception as e:
        raise Exception(f"Error processing chat: {e}")
