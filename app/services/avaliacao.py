from app.schema.schemas import individual_serial
from app.database.config import avaliacao_collection
from app.models.models import AvalicaoModel, NotasAtributos, ParseAvalicaoModelToDocument
from bson import ObjectId

llms_disponiveis = ["ollama3", "openai", "gemini", "deepseek"]

async def PostAvaliacao(avaliacao: AvalicaoModel):
    if (avaliacao.llm1 not in llms_disponiveis or avaliacao.llm2 not in llms_disponiveis):
        return {"message": "llms inválidas: llm1:{}, llm2:{}".format(avaliacao.llm1, avaliacao.llm2)}
    if (not AtributoIsValid(avaliacao.avaliacao_llm1) or  not AtributoIsValid(avaliacao.avaliacao_llm2)):
        return {"message": "notas dos atributos inválidas"}

    avaliacao_collection.insert_one(ParseAvalicaoModelToDocument(avaliacao=avaliacao))
    return {"message": "Avalicao criada com sucesso"}

async def GetOneAvaliacao(id: str):
    return individual_serial(avaliacao_collection.find_one({"_id":ObjectId(id)}))

def AtributoIsValid(notas: NotasAtributos) -> bool:
    for nome, valor in notas.__dict__.items():
        if valor > 5 or valor < 0:
            return False
    return True

