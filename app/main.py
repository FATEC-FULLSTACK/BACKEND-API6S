from fastapi import FastAPI
from app.routes import chat_router
from app.config import load_environment

# Carrega as variáveis de ambiente
load_environment()

app = FastAPI(title="FastAPI RAG Chatbot")

# Inclui as rotas do chat
app.include_router(chat_router)
