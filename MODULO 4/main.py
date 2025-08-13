from pymongo import MongoClient, errors
import sys

# Configuración de la conexión a MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "biblioteca_db"
COLLECTION_NAME = "libros"

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    coleccion = db[COLLECTION_NAME]
except errors.ConnectionFailure:
    print("No se pudo conectar a MongoDB. Verifica que el servicio esté activo.")
    sys.exit(1)

def agregar_libro():
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()
    estado = input("Estado de lectura (leído/no leído): ").strip().lower()

    if estado not in ("leído", "no leído", "leido", "no leido"):
        print("Estado inválido. Debe ser 'leído' o 'no leído' con o sin tilde.")
        return

    libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "estado": estado
    }
    try:
        coleccion.insert_one(libro)
        print("Libro agregado con éxito.")
    except Exception as e:
        print(f"Error al agregar libro: {e}")

def listar_libros():
    libros = list(coleccion.find())
    if not libros:
        print("No hay libros registrados.")
        return
    for libro in libros:
        print(f"ID: {libro['_id']}\nTítulo: {libro['titulo']}\nAutor: {libro['autor']}\nGénero: {libro['genero']}\nEstado: {libro['estado']}\n{'-'*30}")

def buscar_libros():
    print("Buscar por: 1) Título  2) Autor  3) Género")
    opcion = input("Elige opción: ").strip()
    campo = None
    if opcion == "1":
        campo = "titulo"
    elif opcion == "2":
        campo = "autor"
    elif opcion == "3":
        campo = "genero"
    else:
        print("Opción inválida.")
        return

    valor = input(f"Ingresa {campo}: ").strip()
    filtro = {campo: {"$regex": valor, "$options": "i"}}  # búsqueda insensible a mayúsculas

    resultados = list(coleccion.find(filtro))
    if not resultados:
        print("No se encontraron libros que coincidan.")
        return

    for libro in resultados:
        print(f"ID: {libro['_id']}\nTítulo: {libro['titulo']}\nAutor: {libro['autor']}\nGénero: {libro['genero']}\nEstado: {libro['estado']}\n{'-'*30}")

def actualizar_libro():
    id_buscar = input("Ingresa el ID del libro a modificar: ").strip()
    from bson.objectid import ObjectId

    try:
        obj_id = ObjectId(id_buscar)
    except:
        print("ID inválido.")
        return

    libro = coleccion.find_one({"_id": obj_id})
    if not libro:
        print("No se encontró el libro con ese ID.")
        return

    print("Deja en blanco para no modificar el campo.")
    nuevo_titulo = input(f"Título [{libro['titulo']}]: ").strip()
    nuevo_autor = input(f"Autor [{libro['autor']}]: ").strip()
    nuevo_genero = input(f"Género [{libro['genero']}]: ").strip()
    nuevo_estado = input(f"Estado de lectura [{libro['estado']}]: ").strip().lower()

    update_doc = {}
    if nuevo_titulo:
        update_doc["titulo"] = nuevo_titulo
    if nuevo_autor:
        update_doc["autor"] = nuevo_autor
    if nuevo_genero:
        update_doc["genero"] = nuevo_genero
    if nuevo_estado:
        if nuevo_estado in ("leído", "no leído"):
            update_doc["estado"] = nuevo_estado
        else:
            print("Estado inválido. Debe ser 'leído' o 'no leído'.")
            return

    if update_doc:
        coleccion.update_one({"_id": obj_id}, {"$set": update_doc})
        print("Libro actualizado correctamente.")
    else:
        print("No se modificó ningún campo.")

def eliminar_libro():
    id_buscar = input("Ingresa el ID del libro a eliminar: ").strip()
    from bson.objectid import ObjectId

    try:
        obj_id = ObjectId(id_buscar)
    except:
        print("ID inválido.")
        return

    result = coleccion.delete_one({"_id": obj_id})
    if result.deleted_count:
        print("Libro eliminado.")
    else:
        print("No se encontró el libro con ese ID.")

def menu():
    while True:
        print("\n--- Biblioteca Personal (MongoDB) ---")
        print("1. Agregar nuevo libro")
        print("2. Actualizar información de un libro")
        print("3. Eliminar libro existente")
        print("4. Ver listado de libros")
        print("5. Buscar libros")
        print("6. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            actualizar_libro()
        elif opcion == "3":
            eliminar_libro()
        elif opcion == "4":
            listar_libros()
        elif opcion == "5":
            buscar_libros()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
