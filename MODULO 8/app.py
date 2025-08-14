from flask import Flask, render_template, request, redirect, url_for, flash
import redis, json, uuid
import config
from celery_worker import send_email_task  # tarea Celery

app = Flask(__name__)
app.secret_key = "supersecreto"

# ---- Configuración de Flask-Mail ----
from flask_mail import Mail

app.config["MAIL_SERVER"] = getattr(config, "MAIL_SERVER", "")
app.config["MAIL_PORT"] = getattr(config, "MAIL_PORT", 587)
app.config["MAIL_USERNAME"] = getattr(config, "MAIL_USERNAME", "")
app.config["MAIL_PASSWORD"] = getattr(config, "MAIL_PASSWORD", "")
app.config["MAIL_USE_TLS"] = getattr(config, "MAIL_USE_TLS", True)
app.config["MAIL_USE_SSL"] = getattr(config, "MAIL_USE_SSL", False)
app.config["MAIL_DEFAULT_SENDER"] = getattr(config, "MAIL_DEFAULT_SENDER", "")

mail = Mail(app)

# ---- Conexión a KeyDB ----
client = redis.Redis(
    host=getattr(config, "REDIS_HOST", "localhost"),
    port=getattr(config, "REDIS_PORT", 6060),
    decode_responses=True
)

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
    # orden por título
    libros.sort(key=lambda x: x.get("titulo", "").lower())
    return libros

# ---- Rutas ----
@app.route("/")
def index():
    libros = get_all_books()
    return render_template("index.html", libros=libros)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        estado = normalizar_estado(request.form.get("estado", "").strip())

        errores = []
        if not titulo: errores.append("El título no puede estar vacío.")
        if not autor: errores.append("El autor no puede estar vacío.")
        if not genero: errores.append("El género no puede estar vacío.")
        if not validar_estado(estado): errores.append("Estado inválido. Usa: pendiente, leyendo o leído.")

        if errores:
            for e in errores:
                flash(e, "danger")
            return render_template("agregar.html")

        libro_id = str(uuid.uuid4())
        libro = {"id": libro_id, "titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
        client.set(f"libro:{libro_id}", json.dumps(libro))
        flash("Libro agregado correctamente.", "success")

        # Email asíncrono (Celery)
        to_email = getattr(config, "NOTIFY_EMAIL", None)
        if to_email:
            subject = "Nuevo libro agregado"
            body = f"Se agregó el libro: {titulo} (Autor: {autor})"
            send_email_task.delay(to_email, subject, body)

        return redirect(url_for("index"))
    return render_template("agregar.html")

@app.route("/editar/<libro_id>", methods=["GET", "POST"])
def editar(libro_id):
    key = f"libro:{libro_id}"
    raw = client.get(key)
    if not raw:
        flash("Libro no encontrado.", "warning")
        return redirect(url_for("index"))

    libro = json.loads(raw)

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        autor = request.form.get("autor", "").strip()
        genero = request.form.get("genero", "").strip()
        estado = normalizar_estado(request.form.get("estado", "").strip())

        errores = []
        if not titulo: errores.append("El título no puede estar vacío.")
        if not autor: errores.append("El autor no puede estar vacío.")
        if not genero: errores.append("El género no puede estar vacío.")
        if not validar_estado(estado): errores.append("Estado inválido. Usa: pendiente, leyendo o leído.")

        if errores:
            for e in errores:
                flash(e, "danger")
            libro.update({"titulo": titulo, "autor": autor, "genero": genero, "estado": estado})
            return render_template("actualizar.html", libro=libro)

        libro.update({"titulo": titulo, "autor": autor, "genero": genero, "estado": estado})
        client.set(key, json.dumps(libro))
        flash("Libro editado correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("actualizar.html", libro=libro)

@app.route("/eliminar/<libro_id>", methods=["POST"])
def eliminar(libro_id):
    key = f"libro:{libro_id}"
    raw = client.get(key)
    if not raw:
        flash("Libro no encontrado.", "warning")
        return redirect(url_for("index"))

    libro = json.loads(raw)
    borrado = client.delete(key)
    if borrado:
        flash("Libro eliminado.", "success")

        # Email asíncrono (Celery)
        to_email = getattr(config, "NOTIFY_EMAIL", None)
        if to_email:
            subject = "Libro eliminado"
            body = f"Se eliminó el libro: {libro.get('titulo','(sin título)')}."
            send_email_task.delay(to_email, subject, body)
    else:
        flash("No se pudo eliminar el libro.", "danger")

    return redirect(url_for("index"))

@app.route("/buscar", methods=["GET"])
def buscar():
    filtro = request.args.get("filtro", "").strip().lower()
    resultados = []
    if filtro:
        for libro in get_all_books():
            if (
                filtro in libro.get("titulo", "").lower()
                or filtro in libro.get("autor", "").lower()
                or filtro in libro.get("genero", "").lower()
            ):
                resultados.append(libro)
    return render_template("buscar.html", libros=resultados, filtro=filtro)

if __name__ == "__main__":
    # Verifica conexión a KeyDB al iniciar
    try:
        client.ping()
        print("Conexión a KeyDB exitosa")
    except redis.ConnectionError:
        print("No se pudo conectar a KeyDB")
        raise
    app.run(debug=True)
