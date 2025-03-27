from fastapi import FastAPI
from app.routes.chat_router import chat_router
from app.routes.avaliacao_router import avaliacao_router
from app.config import load_environment

# Carrega as variáveis de ambiente
load_environment()

app = FastAPI(title="API6S")

# Inclui as rotas do chat e avaliacao
app.include_router(chat_router)
app.include_router(avaliacao_router)
