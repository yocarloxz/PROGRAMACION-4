import sqlite3

DB_NAME = "presupuesto.db"


# ===================== CONEXIÓN Y TABLAS =====================
def init_db():
    """Crea la base de datos y las tablas si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabla de presupuestos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    """)

    # Tabla de artículos asociados a presupuestos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            presupuesto_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            descripcion TEXT,
            FOREIGN KEY (presupuesto_id) REFERENCES presupuestos (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ===================== GESTIÓN DE PRESUPUESTOS =====================
def crear_presupuesto():
    nombre = input("Nombre del presupuesto: ").strip()
    fecha = input("Fecha (YYYY-MM-DD): ").strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO presupuestos (nombre, fecha) VALUES (?, ?)", (nombre, fecha))
    conn.commit()
    conn.close()
    print("✅ Presupuesto creado con éxito.")


def listar_presupuestos():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM presupuestos")
    presupuestos = cursor.fetchall()
    conn.close()

    if not presupuestos:
        print("📂 No hay presupuestos registrados.")
        return

    print("\n=== LISTA DE PRESUPUESTOS ===")
    print(f"{'ID':<5}{'Nombre':<30}{'Fecha'}")
    print("-" * 50)
    for p in presupuestos:
        print(f"{p[0]:<5}{p[1]:<30}{p[2]}")
    print()


# ===================== GESTIÓN DE ARTÍCULOS =====================
def registrar_articulo():
    listar_presupuestos()
    try:
        presupuesto_id = int(input("ID del presupuesto al que pertenece: "))
    except ValueError:
        print("❌ Error: Debe ingresar un número válido.")
        return

    nombre = input("Nombre del artículo: ").strip()
    categoria = input("Categoría: ").strip()
    try:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio unitario: "))
    except ValueError:
        print("❌ Error: Cantidad debe ser entero y precio un número decimal.")
        return
    descripcion = input("Descripción: ").strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO articulos (presupuesto_id, nombre, categoria, cantidad, precio, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (presupuesto_id, nombre, categoria, cantidad, precio, descripcion))
    conn.commit()
    conn.close()
    print("✅ Artículo registrado con éxito.")


def listar_articulos():
    listar_presupuestos()
    try:
        presupuesto_id = int(input("Ingrese el ID del presupuesto a listar: "))
    except ValueError:
        print("❌ Error: Debe ingresar un número válido.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articulos WHERE presupuesto_id=?", (presupuesto_id,))
    articulos = cursor.fetchall()
    conn.close()

    if not articulos:
        print("📂 No hay artículos en este presupuesto.")
        return

    print("\n=== ARTÍCULOS DEL PRESUPUESTO ===")
    print(f"{'ID':<5}{'Nombre':<20}{'Categoría':<15}{'Cant.':<7}{'Precio':<10}{'Subtotal':<12}{'Descripción'}")
    print("-" * 90)
    total = 0.0
    for art in articulos:
        cantidad = int(art[4])
        precio = float(art[5])
        subtotal = cantidad * precio
        total += subtotal
        print(f"{art[0]:<5}{art[2]:<20}{art[3]:<15}{cantidad:<7}{precio:<10.2f}{subtotal:<12.2f}{art[6]}")
    print("-" * 90)
    print(f"{'TOTAL:':<62}{total:.2f}\n")


def buscar_articulos():
    listar_presupuestos()
    try:
        presupuesto_id = int(input("ID del presupuesto: "))
    except ValueError:
        print("❌ Error: Debe ingresar un número válido.")
        return

    criterio = input("Buscar por (nombre/categoria): ").strip().lower()
    if criterio not in ["nombre", "categoria"]:
        print("❌ Opción inválida.")
        return

    valor = input(f"Ingrese {criterio}: ").strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM articulos WHERE presupuesto_id=? AND {criterio} LIKE ?",
        (presupuesto_id, "%" + valor + "%")
    )
    articulos = cursor.fetchall()
    conn.close()

    if not articulos:
        print("🔎 No se encontraron resultados.")
        return

    print("\n=== RESULTADOS DE BÚSQUEDA ===")
    for art in articulos:
        print(f"[{art[0]}] {art[2]} | {art[3]} | Cant: {art[4]} | Precio: {art[5]} | {art[6]}")


def editar_articulo():
    try:
        id_articulo = int(input("ID del artículo a editar: "))
    except ValueError:
        print("❌ Error: ID inválido.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articulos WHERE id=?", (id_articulo,))
    articulo = cursor.fetchone()

    if not articulo:
        print("❌ No existe artículo con ese ID.")
        conn.close()
        return

    print("Deje en blanco para no modificar el campo.")
    nuevo_nombre = input(f"Nombre ({articulo[2]}): ").strip() or articulo[2]
    nueva_categoria = input(f"Categoría ({articulo[3]}): ").strip() or articulo[3]
    try:
        nueva_cantidad = input(f"Cantidad ({articulo[4]}): ").strip()
        nueva_cantidad = int(nueva_cantidad) if nueva_cantidad else articulo[4]
        nuevo_precio = input(f"Precio ({articulo[5]}): ").strip()
        nuevo_precio = float(nuevo_precio) if nuevo_precio else articulo[5]
    except ValueError:
        print("❌ Error: valores numéricos inválidos.")
        conn.close()
        return
    nueva_desc = input(f"Descripción ({articulo[6]}): ").strip() or articulo[6]

    cursor.execute("""
        UPDATE articulos
        SET nombre=?, categoria=?, cantidad=?, precio=?, descripcion=?
        WHERE id=?
    """, (nuevo_nombre, nueva_categoria, nueva_cantidad, nuevo_precio, nueva_desc, id_articulo))
    conn.commit()
    conn.close()
    print("✏️ Artículo actualizado con éxito.")


def eliminar_articulo():
    try:
        id_articulo = int(input("ID del artículo a eliminar: "))
    except ValueError:
        print("❌ Error: ID inválido.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articulos WHERE id=?", (id_articulo,))
    conn.commit()
    conn.close()
    print("🗑️ Artículo eliminado.")


# ===================== MENÚ PRINCIPAL =====================
def menu():
    while True:
        print("\n=== SISTEMA DE PRESUPUESTOS ===")
        print("1. Crear presupuesto")
        print("2. Listar presupuestos")
        print("3. Registrar artículo")
        print("4. Listar artículos de un presupuesto")
        print("5. Buscar artículos")
        print("6. Editar artículo")
        print("7. Eliminar artículo")
        print("8. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_presupuesto()
        elif opcion == "2":
            listar_presupuestos()
        elif opcion == "3":
            registrar_articulo()
        elif opcion == "4":
            listar_articulos()
        elif opcion == "5":
            buscar_articulos()
        elif opcion == "6":
            editar_articulo()
        elif opcion == "7":
            eliminar_articulo()
        elif opcion == "8":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    init_db()
    menu()
