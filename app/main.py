from fastapi import FastAPI
from routes.chat_router import chat_router
from routes.avaliacao_router import avalicao_router
from config import load_environment

# Carrega as variáveis de ambiente
load_environment()

app = FastAPI(title="API6S")

# Inclui as rotas do chat e avaliacao
app.include_router(chat_router)
app.include_router(avalicao_router)
