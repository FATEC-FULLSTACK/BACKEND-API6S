from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import chat_router
from app.config import load_environment

# Carrega as variáveis de ambiente
load_environment()

app = FastAPI(title="API6S")

# Configuração do CORS
origins = [
    "http://localhost:5173",  # Origem permitida
    "http://127.0.0.1:5173",  # Se você estiver usando localhost com o IP 127.0.0.1
    "*",  # Você pode usar "*" para permitir todas as origens (não recomendado para produção)
]

# Adicionando o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir origens específicas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Inclui as rotas do chat
app.include_router(chat_router)
