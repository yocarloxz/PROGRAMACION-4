import json

ESTADOS_VALIDOS = {"pendiente", "leyendo", "leído"}

def validar_estado(estado: str) -> bool:
    return estado.strip().lower() in ESTADOS_VALIDOS

def normalizar_estado(valor: str) -> str:
    v = valor.strip().lower()
    return "leído" if v == "leido" else v
