from flask import Flask, jsonify, request
import redis, json, uuid, os

# ---- Configuración de Redis desde variables de entorno ----
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6060))

client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = Flask(__name__)

# ---- Utilidades ----
ESTADOS_VALIDOS = {"pendiente", "leyendo", "leído"}

def validar_estado(estado: str) -> bool:
    return estado.strip().lower() in ESTADOS_VALIDOS

def normalizar_estado(valor: str) -> str:
    v = valor.strip().lower()
    return "leído" if v == "leido" else v

def get_all_books():
    keys = client.keys("libro:*")
    libros = []
    for k in keys:
        raw = client.get(k)
        if raw:
            try:
                libros.append(json.loads(raw))
            except json.JSONDecodeError:
                pass
    libros.sort(key=lambda x: x.get("titulo", "").lower())
    return libros

# ---- Rutas API ----
@app.route("/books", methods=["GET"])
def api_get_books():
    return jsonify(get_all_books()), 200

@app.route("/books/<libro_id>", methods=["GET"])
def api_get_book(libro_id):
    raw = client.get(f"libro:{libro_id}")
    if not raw:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify(json.loads(raw)), 200

@app.route("/books", methods=["POST"])
def api_add_book():
    data = request.get_json()
    titulo = data.get("titulo", "").strip()
    autor = data.get("autor", "").strip()
    genero = data.get("genero", "").strip()
    estado = normalizar_estado(data.get("estado", "").strip())

    errores = []
    if not titulo: errores.append("El título no puede estar vacío.")
    if not autor: errores.append("El autor no puede estar vacío.")
    if not genero: errores.append("El género no puede estar vacío.")
    if not validar_estado(estado): errores.append("Estado inválido. Usa: pendiente, leyendo o leído.")

    if errores:
        return jsonify({"errors": errores}), 400

    libro_id = str(uuid.uuid4())
    libro = {"id": libro_id, "titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
    client.set(f"libro:{libro_id}", json.dumps(libro))
    return jsonify(libro), 201

@app.route("/books/<libro_id>", methods=["PUT"])
def api_update_book(libro_id):
    key = f"libro:{libro_id}"
    raw = client.get(key)
    if not raw:
        return jsonify({"error": "Libro no encontrado"}), 404

    data = request.get_json()
    libro = json.loads(raw)

    titulo = data.get("titulo", libro["titulo"]).strip()
    autor = data.get("autor", libro["autor"]).strip()
    genero = data.get("genero", libro["genero"]).strip()
    estado = normalizar_estado(data.get("estado", libro["estado"]).strip())

    errores = []
    if not titulo: errores.append("El título no puede estar vacío.")
    if not autor: errores.append("El autor no puede estar vacío.")
    if not genero: errores.append("El género no puede estar vacío.")
    if not validar_estado(estado): errores.append("Estado inválido. Usa: pendiente, leyendo o leído.")
    if errores:
        return jsonify({"errors": errores}), 400

    libro.update({"titulo": titulo, "autor": autor, "genero": genero, "estado": estado})
    client.set(key, json.dumps(libro))
    return jsonify(libro), 200

@app.route("/books/<libro_id>", methods=["DELETE"])
def api_delete_book(libro_id):
    key = f"libro:{libro_id}"
    raw = client.get(key)
    if not raw:
        return jsonify({"error": "Libro no encontrado"}), 404
    client.delete(key)
    return jsonify({"message": "Libro eliminado"}), 200

# ---- Arranque ----
if __name__ == "__main__":
    try:
        client.ping()
        print("Conexión a Redis exitosa")
    except redis.ConnectionError:
        print("No se pudo conectar a Redis")
        raise
    app.run(debug=True, port=5001)
