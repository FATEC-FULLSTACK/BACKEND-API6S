from fastapi import APIRouter
from app.services.avaliacao import GetOneAvaliacao, PostAvaliacao
from app.models.models import AvaliacaoModel

avaliacao_router = APIRouter(prefix="/avaliacao")

@avaliacao_router.post("/")
async def CreateAvaliacao(avaliacao: AvaliacaoModel):
    return await PostAvaliacao(avaliacao=avaliacao)

@avaliacao_router.get("/{id}")
async def FindOneAvaliacao(id:str):
    return await GetOneAvaliacao(id=id)