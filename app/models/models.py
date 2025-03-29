from typing import Optional
from pydantic import BaseModel, field_validator, Field

class ChatRequest(BaseModel):
    user_id: str
    message: str

class NotasAtributos(BaseModel): 
    coerencia: int = Field(..., ge=0, le=5, description="Valor entre 0 e 5 para coerência")
    respeito: int = Field(..., ge=0, le=5, description="Valor entre 0 e 5 para respeito")
    acuracia: int = Field(..., ge=0, le=5, description="Valor entre 0 e 5 para acurácia")
    relevancia: int = Field(..., ge=0, le=5, description="Valor entre 0 e 5 para relevância")
    veracidade: int = Field(..., ge=0, le=5, description="Valor entre 0 e 5 para veracidade")

class AvaliacaoModel(BaseModel):
    llm1: str
    llm2: str
    endereco_ip_user: str
    pergunta: str
    resposta_llm1:str
    resposta_llm2: str
    avaliacao_llm1: NotasAtributos
    avaliacao_llm2: NotasAtributos
    feedback_usuario: str
    melhor_performance: str

def ParseAvaliacaoModelToDocument(avaliacao: AvaliacaoModel):
    return {
        "llm1": avaliacao.llm1,
        "llm2": avaliacao.llm2,
        "endereco_ip_user": avaliacao.endereco_ip_user,
        "pergunta": avaliacao.pergunta,
        "resposta_llm1": avaliacao.resposta_llm1,
        "resposta_llm2": avaliacao.resposta_llm2,
        "avaliacao_llm1": dict(avaliacao.avaliacao_llm1),
        "avaliacao_llm2": dict(avaliacao.avaliacao_llm2),
        "feedback_usuario": avaliacao.feedback_usuario,
        "melhor_performance": avaliacao.melhor_performance
    }