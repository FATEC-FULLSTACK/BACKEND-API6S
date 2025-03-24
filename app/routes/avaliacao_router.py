from fastapi import APIRouter
from services.avaliacao import GetOneAvaliacao, PostAvaliacao
from models.models import AvalicaoModel

avalicao_router = APIRouter(prefix="/avalicao")

@avalicao_router.post("/")
async def CreateAvalicao(avalicao: AvalicaoModel):
    return await PostAvaliacao(avaliacao=avalicao)

@avalicao_router.get("/{id}")
async def FindOneAvalicao(id:str):
    return await GetOneAvaliacao(id=id)