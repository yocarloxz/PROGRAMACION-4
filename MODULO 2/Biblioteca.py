import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect("biblioteca.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    genero TEXT NOT NULL,
    estado_lectura TEXT CHECK(estado_lectura IN ('leido', 'no leido')) NOT NULL
)
""")
conn.commit()

# Función para agregar un nuevo libro
def agregar_libro():
    titulo = input("Título del libro: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado de lectura (leido/no leido): ").lower()
    if estado not in ['leido', 'no leido']:
        print("Estado inválido. Usa 'leido' o 'no leido'.")
        return
    cursor.execute("INSERT INTO libros (titulo, autor, genero, estado_lectura) VALUES (?, ?, ?, ?)",
                   (titulo, autor, genero, estado))
    conn.commit()
    print(" Libro agregado con éxito.\n")

# Función para actualizar información de un libro
def actualizar_libro():
    listar_libros()
    try:
        libro_id = int(input("ID del libro a actualizar: "))
        campo = input("Campo a actualizar (titulo, autor, genero, estado_lectura): ").lower()
        if campo not in ['titulo', 'autor', 'genero', 'estado_lectura']:
            print("Campo no válido.")
            return
        nuevo_valor = input(f"Nuevo valor para {campo}: ")
        cursor.execute(f"UPDATE libros SET {campo} = ? WHERE id = ?", (nuevo_valor, libro_id))
        conn.commit()
        print(" Libro actualizado correctamente.\n")
    except ValueError:
        print(" Entrada inválida.")

# Función para eliminar un libro
def eliminar_libro():
    listar_libros()
    try:
        libro_id = int(input("ID del libro a eliminar: "))
        cursor.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
        conn.commit()
        print(" Libro eliminado.\n")
    except ValueError:
        print(" Entrada inválida.")

# Función para listar todos los libros
def listar_libros():
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    if libros:
        print("\n Listado de libros:")
        for libro in libros:
            print(f"[{libro[0]}] {libro[1]} - {libro[2]} | {libro[3]} | Estado: {libro[4]}")
        print()
    else:
        print("No hay libros registrados.\n")

# Función para buscar libros
def buscar_libros():
    criterio = input("Buscar por (titulo, autor, genero): ").lower()
    if criterio not in ['titulo', 'autor', 'genero']:
        print("Criterio inválido.")
        return
    valor = input(f"Valor de {criterio}: ")
    cursor.execute(f"SELECT * FROM libros WHERE {criterio} LIKE ?", (f"%{valor}%",))
    resultados = cursor.fetchall()
    if resultados:
        print("\n Resultados de búsqueda:")
        for libro in resultados:
            print(f"[{libro[0]}] {libro[1]} - {libro[2]} | {libro[3]} | Estado: {libro[4]}")
        print()
    else:
        print("No se encontraron libros con ese criterio.\n")

# Menú interactivo
def menu():
    while True:
        print("""
======  BIBLIOTECA PERSONAL ======
1. Agregar nuevo libro
2. Actualizar información de un libro
3. Eliminar libro
4. Ver listado de libros
5. Buscar libros
6. Salir
""")
        opcion = input("Selecciona una opción (1-6): ")
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
            print(" ¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

    conn.close()

if __name__ == "__main__":
    menu()
