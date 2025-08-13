import redis
import json
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6060))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

try:
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    client.ping()
    print("Conectado a KeyDB")
except redis.ConnectionError:
    print("No se pudo conectar a KeyDB. Verifica que esté activo y la configuración.")
    exit(1)

def pedir_campo(nombre):
    valor = ""
    while not valor.strip():
        valor = input(f"{nombre}: ").strip()
        if not valor:
            print(f"El campo '{nombre}' no puede estar vacío.")
    return valor

def pedir_estado(estado_actual=None):
    valores_validos = ["pendiente", "leyendo", "leído", "leido"]
    while True:
        prompt = "Estado de lectura (pendiente, leyendo, leído)"
        if estado_actual:
            prompt += f" [{estado_actual}]"
        estado = input(f"{prompt}: ").strip().lower()
        if not estado and estado_actual:
            return estado_actual
        if estado in valores_validos:
            return estado
        print(f"Valor inválido. Debes escribir exactamente: {', '.join(valores_validos)}")

def agregar_libro():
    libro_id = str(uuid.uuid4())
    titulo = pedir_campo("Título")
    autor = pedir_campo("Autor")
    genero = pedir_campo("Género")
    estado = pedir_estado()

    libro = {
        "id": libro_id,
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }

    key = f"libro:{libro_id}"
    client.set(key, json.dumps(libro))
    print(f"Libro agregado con ID {libro_id}")

def actualizar_libro():
    libro_id = pedir_campo("ID del libro a actualizar")
    key = f"libro:{libro_id}"
    libro_json = client.get(key)
    if not libro_json:
        print("Libro no encontrado.")
        return

    libro = json.loads(libro_json)
    print("Deja en blanco para no modificar un campo.")

    titulo = input(f"Título [{libro['titulo']}]: ").strip()
    autor = input(f"Autor [{libro['autor']}]: ").strip()
    genero = input(f"Género [{libro['genero']}]: ").strip()
    estado = pedir_estado(libro['estado'])

    if titulo:
        libro['titulo'] = titulo
    if autor:
        libro['autor'] = autor
    if genero:
        libro['genero'] = genero
    libro['estado'] = estado

    client.set(key, json.dumps(libro))
    print("Libro actualizado.")

def eliminar_libro():
    libro_id = pedir_campo("ID del libro a eliminar")
    key = f"libro:{libro_id}"
    if client.delete(key):
        print("Libro eliminado.")
    else:
        print("Libro no encontrado.")

def listar_libros():
    keys = client.keys("libro:*")
    if not keys:
        print("No hay libros registrados.")
        return

    for key in keys:
        libro = json.loads(client.get(key))
        print(f"ID: {libro['id']}\nTítulo: {libro['titulo']}\nAutor: {libro['autor']}\nGénero: {libro['genero']}\nEstado: {libro['estado']}\n{'-'*30}")

def buscar_libros():
    filtro = pedir_campo("Buscar por título, autor o género").lower()
    keys = client.keys("libro:*")
    encontrados = []

    for key in keys:
        libro = json.loads(client.get(key))
        if (filtro in libro['titulo'].lower() or
            filtro in libro['autor'].lower() or
            filtro in libro['genero'].lower()):
            encontrados.append(libro)

    if not encontrados:
        print("No se encontraron libros con ese filtro.")
    else:
        for libro in encontrados:
            print(f"ID: {libro['id']}\nTítulo: {libro['titulo']}\nAutor: {libro['autor']}\nGénero: {libro['genero']}\nEstado: {libro['estado']}\n{'-'*30}")

def main():
    while True:
        print("\n-- Biblioteca KeyDB --")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
        print("4. Listar libros")
        print("5. Buscar libros")
        print("6. Salir")

        opcion = input("Elige una opción: ").strip()
        if opcion == '1':
            agregar_libro()
        elif opcion == '2':
            actualizar_libro()
        elif opcion == '3':
            eliminar_libro()
        elif opcion == '4':
            listar_libros()
        elif opcion == '5':
            buscar_libros()
        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()

