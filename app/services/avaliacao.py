from app.schema.schemas import individual_serial
from app.database.config import avaliacao_collection
from app.models.models import AvaliacaoModel, NotasAtributos, ParseAvaliacaoModelToDocument
from bson import ObjectId
from app.utils.validacao import validar_atributos

llms_disponiveis = ["ollama3", "openai", "gemini", "deepseek"]

async def PostAvaliacao(avaliacao: AvaliacaoModel):
    if (avaliacao.llm1 not in llms_disponiveis or avaliacao.llm2 not in llms_disponiveis):
        return {"message": "llms inválidas: llm1:{}, llm2:{}".format(avaliacao.llm1, avaliacao.llm2)}
    if (not AtributoIsValid(avaliacao.avaliacao_llm1) or  not AtributoIsValid(avaliacao.avaliacao_llm2)):
        return {"message": "notas dos atributos inválidas"}

    avaliacao_collection.insert_one(ParseAvaliacaoModelToDocument(avaliacao=avaliacao))
    return {"message": "Avaliacao criada com sucesso"}

async def GetOneAvaliacao(id: str):
    return individual_serial(avaliacao_collection.find_one({"_id":ObjectId(id)}))

def AtributoIsValid(avaliacao: NotasAtributos) -> bool:
    try:
        validar_atributos(avaliacao)
        return True
    except ValueError:
        return False