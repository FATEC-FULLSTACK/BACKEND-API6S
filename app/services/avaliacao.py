from app.schema.schemas import individual_serial
from app.database.config import avaliacao_collection
from app.models.models import AvaliacaoModel, Avaliacao, ParseAvaliacaoModelToDocument
from bson import ObjectId
from app.utils.validacao import validar_atributos

llms_disponiveis = ["ollama3", "openai", "gemini", "deepseek", "groq"]

async def PostAvaliacao(avaliacao: AvaliacaoModel):
    if (avaliacao.llm1 not in llms_disponiveis or avaliacao.llm2 not in llms_disponiveis):
        return {"message": "llms inválidas: llm1:{}, llm2:{}".format(avaliacao.llm1, avaliacao.llm2)}
    if (not AtributoIsValid(avaliacao.avaliacao_llm1) or  not AtributoIsValid(avaliacao.avaliacao_llm2)):
        return {"message": "notas dos atributos inválidas"}

    avaliacao_collection.insert_one(ParseAvaliacaoModelToDocument(avaliacao=avaliacao))
    return {"message": "Avaliacao criada com sucesso"}

async def GetOneAvaliacao(id: str):
    return individual_serial(avaliacao_collection.find_one({"_id":ObjectId(id)}))

async def PutAvaliacao(id: str, avaliacao: AvaliacaoModel):
    if (avaliacao.llm1 not in llms_disponiveis or avaliacao.llm2 not in llms_disponiveis):
        return {"message": "llms inválidas: llm1:{}, llm2:{}".format(avaliacao.llm1, avaliacao.llm2)}
    
    if not AtributoIsValid(avaliacao.avaliacao_llm1) or not AtributoIsValid(avaliacao.avaliacao_llm2):
        return {"message": "notas dos atributos inválidas"}
    
    result = avaliacao_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": ParseAvaliacaoModelToDocument(avaliacao=avaliacao)}
    )
    
    if result.matched_count > 0:
        return {"message": "Avaliação atualizada com sucesso"}
    else:
        return {"message": "Avaliação não encontrada"}
    
async def RemoveAvaliacao(id: str):
    result = avaliacao_collection.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count > 0:
        return {"message": "Avaliação deletada com sucesso"}
    else:
        return {"message": "Avaliação não encontrada"}

def AtributoIsValid(avaliacao: Avaliacao) -> bool:
    try:
        validar_atributos(avaliacao)
        return True
    except ValueError:
        return False

async def GetDesempenhoAvaliacao():
    pipeline = [
        {
            "$facet": {
                "participacao": [
                    {
                        "$project": {
                            "llms": ["$llm1", "$llm2"]
                        }
                    },
                    {
                        "$unwind": "$llms"
                    },
                    {
                        "$group": {
                            "_id": "$llms",
                            "total_participacao": {"$sum": 1}
                        }
                    }
                ],
                "melhor_performance": [
                    {
                        "$match": {
                            "melhor_performance": {"$ne": None}
                        }
                    },
                    {
                        "$group": {
                            "_id": "$melhor_performance",
                            "total_melhor_performance": {"$sum": 1}
                        }
                    }
                ]
            }
        },
        {
            "$project": {
                "merged": {
                    "$concatArrays": ["$participacao", "$melhor_performance"]
                }
            }
        },
        {
            "$unwind": "$merged"
        },
        {
            "$group": {
                "_id": "$merged._id",
                "total_participacao": {"$max": "$merged.total_participacao"},
                "total_melhor_performance": {"$max": "$merged.total_melhor_performance"}
            }
        },
        {
            "$project": {
                "nome_llm": "$_id",
                "total_participacao": {
                    "$ifNull": ["$total_participacao", 0]
                },
                "total_melhor_performance": {
                    "$ifNull": ["$total_melhor_performance", 0]
                },
                "_id": 0
            }
        },
        {
            "$sort": {
                "nome_llm": 1
            }
        }
    ]

    resultado = list(avaliacao_collection.aggregate(pipeline))
    return resultado
