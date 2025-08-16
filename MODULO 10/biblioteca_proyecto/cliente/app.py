from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from config import Config  # Carga SECRET_KEY y API_URL

app = Flask(__name__)
app.config.from_object(Config)

# ---- Utilidades ----
ESTADOS_VALIDOS = {"pendiente", "leyendo", "leído"}

def validar_estado(estado: str) -> bool:
    return estado.strip().lower() in ESTADOS_VALIDOS

def normalizar_estado(valor: str) -> str:
    v = valor.strip().lower()
    return "leído" if v == "leido" else v

# ---- Rutas Flask ----
@app.route("/")
def index():
    try:
        r = requests.get(f"{app.config['API_URL']}/books")
        r.raise_for_status()
        libros = r.json()
    except Exception as e:
        libros = []
        flash(f"No se pudo conectar a la API: {e}", "danger")
    return render_template("index.html", libros=libros)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        data = {
            "titulo": request.form.get("titulo", "").strip(),
            "autor": request.form.get("autor", "").strip(),
            "genero": request.form.get("genero", "").strip(),
            "estado": normalizar_estado(request.form.get("estado", "").strip())
        }

        errores = [f"{campo} no puede estar vacío." for campo in ["titulo", "autor", "genero", "estado"] if not data[campo]]
        if not validar_estado(data["estado"]):
            errores.append("Estado inválido. Usa: pendiente, leyendo o leído.")

        if errores:
            for e in errores:
                flash(e, "danger")
            return render_template("agregar.html")

        try:
            r = requests.post(f"{app.config['API_URL']}/books", json=data)
            if r.status_code in (200, 201):
                flash("Libro agregado correctamente.", "success")
                return redirect(url_for("index"))
            else:
                flash(f"Error API: {r.json()}", "danger")
        except Exception as e:
            flash(f"No se pudo conectar a la API: {e}", "danger")

    return render_template("agregar.html")

@app.route("/editar/<libro_id>", methods=["GET", "POST"])
def editar(libro_id):
    try:
        r = requests.get(f"{app.config['API_URL']}/books/{libro_id}")
        r.raise_for_status()
        libro = r.json()
    except Exception:
        flash("Libro no encontrado o no se pudo conectar a la API.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        data = {
            "titulo": request.form.get("titulo", "").strip(),
            "autor": request.form.get("autor", "").strip(),
            "genero": request.form.get("genero", "").strip(),
            "estado": normalizar_estado(request.form.get("estado", "").strip())
        }

        errores = [f"{campo} no puede estar vacío." for campo in ["titulo", "autor", "genero", "estado"] if not data[campo]]
        if not validar_estado(data["estado"]):
            errores.append("Estado inválido.")

        if errores:
            for e in errores:
                flash(e, "danger")
            libro.update(data)
            return render_template("actualizar.html", libro=libro)

        try:
            r = requests.put(f"{app.config['API_URL']}/books/{libro_id}", json=data)
            if r.status_code == 200:
                flash("Libro editado correctamente.", "success")
                return redirect(url_for("index"))
            else:
                flash(f"Error API: {r.json()}", "danger")
        except Exception as e:
            flash(f"No se pudo conectar a la API: {e}", "danger")

    return render_template("actualizar.html", libro=libro)

@app.route("/eliminar/<libro_id>", methods=["POST"])
def eliminar(libro_id):
    try:
        r = requests.delete(f"{app.config['API_URL']}/books/{libro_id}")
        if r.status_code == 200:
            flash("Libro eliminado.", "success")
        else:
            flash(f"Error API: {r.json()}", "danger")
    except Exception as e:
        flash(f"No se pudo conectar a la API: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/buscar", methods=["GET"])
def buscar():
    filtro = request.args.get("filtro", "").strip().lower()
    resultados = []
    if filtro:
        try:
            r = requests.get(f"{app.config['API_URL']}/books")
            r.raise_for_status()
            for libro in r.json():
                if filtro in libro.get("titulo", "").lower() or filtro in libro.get("autor", "").lower() or filtro in libro.get("genero", "").lower():
                    resultados.append(libro)
        except Exception:
            flash("No se pudo conectar a la API", "danger")
    return render_template("buscar.html", libros=resultados, filtro=filtro)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
