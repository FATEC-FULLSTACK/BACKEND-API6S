from typing import List
from app.models.models import Avaliacao

VALID_FIELDS = ["relevancia", "acuracia", "veracidade", "coerencia", "respeito", "idioma"]

def validar_atributos(notas: Avaliacao) -> bool:
    campos_invalidos = [nome for nome in notas.dict().keys() if nome not in VALID_FIELDS]
    
    if campos_invalidos:
        raise ValueError(f"Atributos inválidos: {', '.join(campos_invalidos)}")
    return True