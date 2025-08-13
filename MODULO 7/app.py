from flask import Flask, render_template, request, redirect, url_for, flash
import redis, json, uuid
import config

app = Flask(__name__)
app.secret_key = "supersecreto"

client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    decode_responses=True
)

try:
    client.ping()
    print("conexion exitosa")
except redis.ConnectionError:
    print("No se pudo conectar a KeyDB")
    exit(1)
def validar_estado(estado):
    estados_validos = ["pendiente", "leyendo", "leído"]
    return estado.lower() in estados_validos

@app.route("/")
def index():
    keys = client.keys("libro:*")
    libros = [json.loads(client.get(k)) for k in keys]
    return render_template("index.html", libros=libros)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        estado = request.form.get("estado", "").strip().lower()

        if not (titulo and autor and genero and estado):
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("agregar"))

        if not validar_estado(estado):
            flash("Estado inválido. Debe ser: pendiente, leyendo o leído.", "error")
            return redirect(url_for("agregar"))

        libro_id = str(uuid.uuid4())
        libro = {"id": libro_id, "titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
        client.set(f"libro:{libro_id}", json.dumps(libro))
        flash("Libro agregado correctamente.", "success")
        return redirect(url_for("index"))
    return render_template("agregar.html")

@app.route("/editar/<libro_id>", methods=["GET", "POST"])
def editar(libro_id):
    key = f"libro:{libro_id}"
    libro_json = client.get(key)
    if not libro_json:
        flash("Libro no encontrado.", "error")
        return redirect(url_for("index"))

    libro = json.loads(libro_json)

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        estado = request.form.get("estado", "").strip().lower()

        if not validar_estado(estado):
            flash("Estado inválido. Debe ser: pendiente, leyendo o leído.", "error")
            return redirect(url_for("actualizar", libro_id=libro_id))

        libro.update({"titulo": titulo, "autor": autor, "genero": genero, "estado": estado})
        client.set(key, json.dumps(libro))
        flash("Libro editado correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("actualizar.html", libro=libro)

@app.route("/eliminar/<libro_id>", methods=["POST"])
def eliminar(libro_id):
    key = f"libro:{libro_id}"
    if client.delete(key):
        flash("Libro eliminado.", "success")
    else:
        flash("Libro no encontrado.", "error")
    return redirect(url_for("index"))

@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    libros_encontrados = []
    if request.method == "POST":
        filtro = request.form.get("filtro", "").strip().lower()
        keys = client.keys("libro:*")
        for k in keys:
            libro = json.loads(client.get(k))
            if filtro in libro["titulo"].lower() or filtro in libro["autor"].lower() or filtro in libro["genero"].lower():
                libros_encontrados.append(libro)
        if not libros_encontrados:
            flash("No se encontraron libros con ese filtro.", "error")
    return render_template("buscar.html", libros=libros_encontrados)

if __name__ == "__main__":
    app.run(debug=True)
