from flask_restful import Resource, reqparse
from . import r
from .models import validar_estado, normalizar_estado
import uuid, json

parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, required=True)
parser.add_argument('autor', type=str, required=True)
parser.add_argument('genero', type=str, required=True)
parser.add_argument('estado', type=str, required=True)

class BookListResource(Resource):
    def get(self):
        keys = r.keys("libro:*")
        libros = [json.loads(r.get(k)) for k in keys if r.get(k)]
        libros.sort(key=lambda x: x.get("titulo","").lower())
        return libros, 200

    def post(self):
        args = parser.parse_args()
        estado = normalizar_estado(args['estado'])
        if not validar_estado(estado):
            return {"error":"Estado inválido"}, 400

        book_id = str(uuid.uuid4())
        libro = {
            "id": book_id,
            "titulo": args['titulo'],
            "autor": args['autor'],
            "genero": args['genero'],
            "estado": estado
        }
        r.set(f"libro:{book_id}", json.dumps(libro))
        return libro, 201

class BookResource(Resource):
    def get(self, book_id):
        raw = r.get(f"libro:{book_id}")
        if not raw:
            return {"error":"Libro no encontrado"}, 404
        return json.loads(raw), 200

    def put(self, book_id):
        raw = r.get(f"libro:{book_id}")
        if not raw:
            return {"error":"Libro no encontrado"}, 404

        args = parser.parse_args()
        estado = normalizar_estado(args['estado'])
        if not validar_estado(estado):
            return {"error":"Estado inválido"}, 400

        libro = json.loads(raw)
        libro.update({
            "titulo": args['titulo'],
            "autor": args['autor'],
            "genero": args['genero'],
            "estado": estado
        })
        r.set(f"libro:{book_id}", json.dumps(libro))
        return libro, 200

    def delete(self, book_id):
        borrado = r.delete(f"libro:{book_id}")
        if borrado:
            return {"mensaje":"Libro eliminado"}, 200
        return {"error":"No se pudo eliminar"}, 404
