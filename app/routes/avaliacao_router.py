from fastapi import APIRouter
from app.services.avaliacao import GetOneAvaliacao, PostAvaliacao, PutAvaliacao, RemoveAvaliacao, GetDesempenhoAvaliacao
from app.models.models import AvaliacaoModel

avaliacao_router = APIRouter(prefix="/avaliacao")

@avaliacao_router.post("/")
async def CreateAvaliacao(avaliacao: AvaliacaoModel):
    return await PostAvaliacao(avaliacao=avaliacao)

# @avaliacao_router.get("/{id}")
# async def FindOneAvaliacao(id:str):
#     return await GetOneAvaliacao(id=id)

@avaliacao_router.put("/{id}")
async def UpdateAvaliacao(id: str, avaliacao: AvaliacaoModel):
    return await PutAvaliacao(id=id, avaliacao=avaliacao)

@avaliacao_router.delete("/{id}")
async def DeleteAvaliacao(id: str):
    return await RemoveAvaliacao(id=iavaliacoes_collectiond)

@avaliacao_router.get("/desempenho")
async def DesempenhoAvaliacao():
    return await GetDesempenhoAvaliacao()