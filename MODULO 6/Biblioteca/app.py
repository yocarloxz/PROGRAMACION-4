from flask import Flask, render_template, request, redirect, url_for, flash
import json, uuid
from config import client

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    keys = client.keys("libro:*")
    libros = [json.loads(client.get(key)) for key in keys]
    return render_template('index.html', libros=libros)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        autor = request.form['autor'].strip()
        genero = request.form['genero'].strip()
        estado = request.form['estado'].strip().lower()

        if not titulo or not autor or not genero or estado not in ['pendiente', 'leyendo', 'leído']:
            flash("Todos los campos son obligatorios y el estado debe ser: pendiente, leyendo o leído.", "danger")
            return redirect(url_for('agregar'))

        libro_id = str(uuid.uuid4())
        libro = {"id": libro_id, "titulo": titulo, "autor": autor, "genero": genero, "estado": estado}
        client.set(f"libro:{libro_id}", json.dumps(libro))
        flash("Libro agregado exitosamente.", "success")
        return redirect(url_for('index'))

    return render_template('agregar.html')

@app.route('/editar/<libro_id>', methods=['GET', 'POST'])
def editar(libro_id):
    key = f"libro:{libro_id}"
    libro_json = client.get(key)
    if not libro_json:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('index'))

    libro = json.loads(libro_json)

    if request.method == 'POST':
        titulo = request.form['titulo'].strip() or libro['titulo']
        autor = request.form['autor'].strip() or libro['autor']
        genero = request.form['genero'].strip() or libro['genero']
        estado = request.form['estado'].strip().lower() or libro['estado']

        if estado not in ['pendiente', 'leyendo', 'leído']:
            flash("El estado debe ser: pendiente, leyendo o leído.", "danger")
            return redirect(url_for('editar', libro_id=libro_id))

        libro.update({"titulo": titulo, "autor": autor, "genero": genero, "estado": estado})
        client.set(key, json.dumps(libro))
        flash("Libro actualizado exitosamente.", "success")
        return redirect(url_for('index'))

    return render_template('editar.html', libro=libro)

@app.route('/eliminar/<libro_id>')
def eliminar(libro_id):
    key = f"libro:{libro_id}"
    if client.delete(key):
        flash("Libro eliminado.", "success")
    else:
        flash("Libro no encontrado.", "danger")
    return redirect(url_for('index'))

@app.route('/buscar', methods=['GET'])
def buscar():
    filtro = request.args.get('q', '').lower()
    keys = client.keys("libro:*")
    encontrados = [
        json.loads(client.get(k)) for k in keys
        if filtro in json.loads(client.get(k))['titulo'].lower() or
           filtro in json.loads(client.get(k))['autor'].lower() or
           filtro in json.loads(client.get(k))['genero'].lower()
    ]
    return render_template('index.html', libros=encontrados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
