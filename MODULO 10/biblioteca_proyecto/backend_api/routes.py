import requests
from flask import current_app as app

API_URL = "http://127.0.0.1:5001"  # URL de tu API REST

ESTADOS_VALIDOS = {"pendiente", "leyendo", "leído"}

def validar_estado(estado: str) -> bool:
    return estado.strip().lower() in ESTADOS_VALIDOS

def normalizar_estado(valor: str) -> str:
    v = valor.strip().lower()
    return "leído" if v == "leido" else v

# ---- Recursos ----

def get_all_books():
    try:
        r = requests.get(f"{API_URL}/books")
        r.raise_for_status()
        libros = r.json()
        libros.sort(key=lambda x: x.get("titulo","").lower())
        return libros
    except Exception as e:
        app.logger.error(f"Error al obtener libros: {e}")
        return []

def get_book(book_id):
    try:
        r = requests.get(f"{API_URL}/books/{book_id}")
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def add_book(data):
    try:
        r = requests.post(f"{API_URL}/books", json=data)
        r.raise_for_status()
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def update_book(book_id, data):
    try:
        r = requests.put(f"{API_URL}/books/{book_id}", json=data)
        r.raise_for_status()
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def delete_book(book_id):
    try:
        r = requests.delete(f"{API_URL}/books/{book_id}")
        r.raise_for_status()
        return {"message": "Libro eliminado"}, r.status_code
    except Exception as e:
        return {"error": str(e)}, 500
