from typing import List
from app.models.models import NotasAtributos

VALID_FIELDS = ["coerencia", "respeito", "acuracia", "relevancia", "veracidade"]

def validar_atributos(notas: NotasAtributos) -> bool:
    campos_invalidos = [nome for nome in notas.dict().keys() if nome not in VALID_FIELDS]
    
    if campos_invalidos:
        raise ValueError(f"Atributos inválidos: {', '.join(campos_invalidos)}")
    return True