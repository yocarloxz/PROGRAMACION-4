from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)


libros_db = {}

# ---- Utilidades ----
ESTADOS_VALIDOS = {"pendiente", "leyendo", "leído"}

def validar_estado(estado: str) -> bool:
    return estado.strip().lower() in ESTADOS_VALIDOS

def normalizar_estado(valor: str) -> str:
    v = valor.strip().lower()
    return "leído" if v == "leido" else v

# ---- Endpoints ----
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(list(libros_db.values())), 200

@app.route("/books/<libro_id>", methods=["GET"])
def get_book(libro_id):
    libro = libros_db.get(libro_id)
    if not libro:
        return jsonify({"error": "Libro no encontrado"}), 404
    return jsonify(libro), 200

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    titulo = data.get("titulo", "").strip()
    autor = data.get("autor", "").strip()
    genero = data.get("genero", "").strip()
    estado = normalizar_estado(data.get("estado", "").strip())

    errores = []
    if not titulo: errores.append("El título no puede estar vacío.")
    if not autor: errores.append("El autor no puede estar vacío.")
    if not genero: errores.append("El género no puede estar vacío.")
    if not validar_estado(estado): errores.append("Estado inválido.")

    if errores:
        return jsonify({"errors": errores}), 400

    libro_id = str(uuid.uuid4())
    libro = {"id": libro_id, "titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
    libros_db[libro_id] = libro
    return jsonify(libro), 201

@app.route("/books/<libro_id>", methods=["PUT"])
def update_book(libro_id):
    libro = libros_db.get(libro_id)
    if not libro:
        return jsonify({"error": "Libro no encontrado"}), 404

    data = request.get_json()
    libro.update({
        "titulo": data.get("titulo", libro["titulo"]).strip(),
        "autor": data.get("autor", libro["autor"]).strip(),
        "genero": data.get("genero", libro["genero"]).strip(),
        "estado": normalizar_estado(data.get("estado", libro["estado"]).strip())
    })
    return jsonify(libro), 200

@app.route("/books/<libro_id>", methods=["DELETE"])
def delete_book(libro_id):
    if libro_id not in libros_db:
        return jsonify({"error": "Libro no encontrado"}), 404
    libros_db.pop(libro_id)
    return jsonify({"message": "Libro eliminado"}), 200

# ---- Run ----
if __name__ == "__main__":
    app.run(debug=True, port=5001)
