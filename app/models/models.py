from typing import Optional
from pydantic import BaseModel, field_validator, Field

class ChatRequest(BaseModel):
    user_id: str
    message: str

class AvaliacaoAtributo(BaseModel):
    rating : int = Field(..., ge=0, le=5, description="Valor de 0 a 5")
    text   : str 

class Avaliacao(BaseModel): 
    relevancia: AvaliacaoAtributo = Field(..., description="Respondeu o que perguntou?")
    acuracia: AvaliacaoAtributo = Field(..., description="Os dados apresentados estão consistentes com as suas expectativas ou conhecimento prévio sobre o assunto?")
    veracidade: AvaliacaoAtributo = Field(..., description="De acordo com a base de dados, ele trouxe fatos ou deu uma opinião?")
    coerencia: AvaliacaoAtributo = Field(..., description="A resposta é bem estruturada e coerente com si mesma?")
    respeito: AvaliacaoAtributo = Field(..., description="A resposta foi ofensiva ou agressiva?")
    idioma: AvaliacaoAtributo = Field(..., description="A resposta foi gerada no idioma correto?")

class AvaliacaoModel(BaseModel):
    llm1: str = Field(default="openai",description="qual llm foi utilizada (ex: openai, gemini, deepseek, ollama)")
    llm2: str = Field(default="gemini",description="qual llm foi utilizada (ex: openai, gemini, deepseek, ollama)")
    endereco_ip_user: str = Field(default="127.0.0.1", description="qual foi o endereço ip que enviou a avalição")
    pergunta: str = Field(...,description="qual foi a pergunta realizada?")
    resposta_llm1:str = Field(...,description="qual foi a resposta da llm1")
    resposta_llm2: str = Field(...,description="qual foi a resposta da llm2")
    avaliacao_llm1: Avaliacao = Field(...,description="avaliação da llm1")
    avaliacao_llm2: Avaliacao = Field(...,description="avaliação da llm1")
    feedback_usuario: str = Field(...,description="feedback geral das respostas das llms")
    melhor_performance: str = Field(...,description="qual llm se performou melhor")

def ParseAvaliacaoModelToDocument(avaliacao: AvaliacaoModel) -> dict:
    # Converte o modelo Pydantic em um dicionário
    avaliacao_dict = avaliacao.dict()

    # Converte explicitamente os objetos AvaliacaoAtributo em dicionários
    if "avaliacao_llm1" in avaliacao_dict:
        avaliacao_dict["avaliacao_llm1"] = {
            k: v.dict() if hasattr(v, "dict") else v
            for k, v in avaliacao_dict["avaliacao_llm1"].items()
        }
    
    if "avaliacao_llm2" in avaliacao_dict:
        avaliacao_dict["avaliacao_llm2"] = {
            k: v.dict() if hasattr(v, "dict") else v
            for k, v in avaliacao_dict["avaliacao_llm2"].items()
        }

    return avaliacao_dict