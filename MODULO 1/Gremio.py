import sqlite3

conn = sqlite3.connect("registro_gremio.db")
cursor = conn.cursor()

# Crear tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS heroes (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    clase TEXT CHECK(clase IN ('Guerrero', 'Mago', 'Arquero', 'Pícaro', 'Clérigo')),
    nivel_experiencia INTEGER CHECK(nivel_experiencia >= 0)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones (
    id INTEGER PRIMARY KEY,
    descripcion TEXT UNIQUE NOT NULL,
    dificultad TEXT CHECK(dificultad IN ('Baja', 'Media', 'Alta')),
    localizacion TEXT,
    recompensa INTEGER CHECK(recompensa >= 0)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS monstruos (
    id INTEGER PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL,
    tipo TEXT CHECK(tipo IN ('Dragón', 'Goblin', 'No-muerto', 'Bestia', 'Demonio')),
    nivel_amenaza INTEGER CHECK(nivel_amenaza BETWEEN 1 AND 10)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones_heroes (
    id INTEGER PRIMARY KEY,
    mision_id INTEGER NOT NULL,
    heroe_id INTEGER NOT NULL,
    FOREIGN KEY (mision_id) REFERENCES misiones(id),
    FOREIGN KEY (heroe_id) REFERENCES heroes(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS misiones_monstruos (
    id INTEGER PRIMARY KEY,
    mision_id INTEGER NOT NULL,
    monstruo_id INTEGER NOT NULL,
    FOREIGN KEY (mision_id) REFERENCES misiones(id),
    FOREIGN KEY (monstruo_id) REFERENCES monstruos(id)
);
""")

# Función para insertar si no existe (héroes)
def insertar_heroe(nombre, clase, nivel_experiencia):
    cursor.execute("SELECT id FROM heroes WHERE nombre = ?", (nombre,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO heroes (nombre, clase, nivel_experiencia) VALUES (?, ?, ?)",
                       (nombre, clase, nivel_experiencia))
        print(f"Héroe '{nombre}' insertado.")
    else:
        print(f"Héroe '{nombre}' ya existe.")

# Función para insertar si no existe (misiones)
def insertar_mision(descripcion, dificultad, localizacion, recompensa):
    cursor.execute("SELECT id FROM misiones WHERE descripcion = ?", (descripcion,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO misiones (descripcion, dificultad, localizacion, recompensa) VALUES (?, ?, ?, ?)",
                       (descripcion, dificultad, localizacion, recompensa))
        print(f"Misión '{descripcion}' insertada.")
    else:
        print(f"Misión '{descripcion}' ya existe.")

# Función para insertar si no existe (monstruos)
def insertar_monstruo(nombre, tipo, nivel_amenaza):
    cursor.execute("SELECT id FROM monstruos WHERE nombre = ?", (nombre,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO monstruos (nombre, tipo, nivel_amenaza) VALUES (?, ?, ?)",
                       (nombre, tipo, nivel_amenaza))
        print(f"Monstruo '{nombre}' insertado.")
    else:
        print(f"Monstruo '{nombre}' ya existe.")

# Función para obtener ID por campo y valor
def obtener_id(tabla, campo, valor):
    cursor.execute(f"SELECT id FROM {tabla} WHERE {campo} = ?", (valor,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None

# Función para asociar héroe y misión
def asociar_heroe_mision(nombre_heroe, descripcion_mision):
    heroe_id = obtener_id("heroes", "nombre", nombre_heroe)
    mision_id = obtener_id("misiones", "descripcion", descripcion_mision)
    if heroe_id and mision_id:
        cursor.execute("SELECT id FROM misiones_heroes WHERE heroe_id = ? AND mision_id = ?", (heroe_id, mision_id))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO misiones_heroes (mision_id, heroe_id) VALUES (?, ?)", (mision_id, heroe_id))
            print(f"Asociación héroe '{nombre_heroe}' con misión '{descripcion_mision}' creada.")
        else:
            print(f"Asociación héroe '{nombre_heroe}' con misión '{descripcion_mision}' ya existe.")

# Función para asociar monstruo y misión
def asociar_monstruo_mision(nombre_monstruo, descripcion_mision):
    monstruo_id = obtener_id("monstruos", "nombre", nombre_monstruo)
    mision_id = obtener_id("misiones", "descripcion", descripcion_mision)
    if monstruo_id and mision_id:
        cursor.execute("SELECT id FROM misiones_monstruos WHERE monstruo_id = ? AND mision_id = ?", (monstruo_id, mision_id))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO misiones_monstruos (mision_id, monstruo_id) VALUES (?, ?)", (mision_id, monstruo_id))
            print(f"Asociación monstruo '{nombre_monstruo}' con misión '{descripcion_mision}' creada.")
        else:
            print(f"Asociación monstruo '{nombre_monstruo}' con misión '{descripcion_mision}' ya existe.")

# Datos fijos a insertar
heroes = [
    ("Luna", "Mago", 20),
    ("Thorn", "Arquero", 15),
    ("Aldric", "Guerrero", 12),
]

misiones = [
    ("Proteger el pueblo de los goblins", "Media", "Bosque Sombrío", 200),
    ("Derrotar al dragón escarlata", "Alta", "Montañas Ardientes", 500),
]

monstruos = [
    ("Goblin Guerrero", "Goblin", 3),
    ("Dragón Escarlata", "Dragón", 10),
]

# Insertar datos
for h in heroes:
    insertar_heroe(*h)

for m in misiones:
    insertar_mision(*m)

for mo in monstruos:
    insertar_monstruo(*mo)

# Crear asociaciones
asociar_heroe_mision("Luna", "Proteger el pueblo de los goblins")
asociar_heroe_mision("Thorn", "Proteger el pueblo de los goblins")
asociar_heroe_mision("Luna", "Derrotar al dragón escarlata")

asociar_monstruo_mision("Goblin Guerrero", "Proteger el pueblo de los goblins")
asociar_monstruo_mision("Dragón Escarlata", "Derrotar al dragón escarlata")

conn.commit()
conn.close()
