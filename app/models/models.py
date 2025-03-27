from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str

# O nome dos campos vão mudar quando descobrirmos o quais serão os atributos
class NotasAtributos(BaseModel):
    atributo1: int
    atributo2: int
    atributo3: int
    atributo4: int
    atributo5: int

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