from Database import SessionLocal, engine
from models import Base, Libro

# Crea las tablas en la base de datos (solo una vez)
Base.metadata.create_all(bind=engine)


def agregar_libro():
    session = SessionLocal()
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        genero = input("Género: ")
        estado = input("Estado (leído/no leído): ")

        nuevo_libro = Libro(titulo=titulo, autor=autor, genero=genero, estado=estado)
        session.add(nuevo_libro)
        session.commit()
        print("Libro agregado exitosamente.")
    except Exception as e:
        print("Error:", e)
        session.rollback()
    finally:
        session.close()


def listar_libros():
    session = SessionLocal()
    libros = session.query(Libro).all()
    for libro in libros:
        print(libro)
    session.close()


def buscar_libro():
    session = SessionLocal()
    campo = input("Buscar por (titulo/autor/genero): ").lower()
    valor = input("Valor a buscar: ")

    filtros = {
        "titulo": Libro.titulo,
        "autor": Libro.autor,
        "genero": Libro.genero
    }

    if campo in filtros:
        resultados = session.query(Libro).filter(filtros[campo].like(f"%{valor}%")).all()
        for libro in resultados:
            print(libro)
    else:
        print("Campo no válido.")
    session.close()


def actualizar_libro():
    session = SessionLocal()
    try:
        id_libro = int(input("ID del libro a actualizar: "))
        libro = session.query(Libro).get(id_libro)
        if libro:
            print(f"Libro actual: {libro}")
            libro.titulo = input("Nuevo título: ") or libro.titulo
            libro.autor = input("Nuevo autor: ") or libro.autor
            libro.genero = input("Nuevo género: ") or libro.genero
            libro.estado = input("Nuevo estado (leído/no leído): ") or libro.estado
            session.commit()
            print("Libro actualizado.")
        else:
            print("Libro no encontrado.")
    except Exception as e:
        print("Error:", e)
        session.rollback()
    finally:
        session.close()


def eliminar_libro():
    session = SessionLocal()
    try:
        id_libro = int(input("ID del libro a eliminar: "))
        libro = session.query(Libro).get(id_libro)
        if libro:
            session.delete(libro)
            session.commit()
            print("Libro eliminado.")
        else:
            print("Libro no encontrado.")
    except Exception as e:
        print("Error:", e)
        session.rollback()
    finally:
        session.close()


def menu():
    while True:
        print("\nMENÚ BIBLIOTECA")
        print("1. Agregar libro")
        print("2. Listar libros")
        print("3. Buscar libro")
        print("4. Actualizar libro")
        print("5. Eliminar libro")
        print("6. Salir")

        opcion = input("Elige una opción: ")
        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            listar_libros()
        elif opcion == "3":
            buscar_libro()
        elif opcion == "4":
            actualizar_libro()
        elif opcion == "5":
            eliminar_libro()
        elif opcion == "6":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
