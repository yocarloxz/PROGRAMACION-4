# Biblioteca Web con Flask y KeyDB

Aplicación web para gestionar una biblioteca personal usando Flask como framework web y KeyDB como almacenamiento en memoria. Permite agregar, actualizar, eliminar, listar y buscar libros mediante una interfaz web.

## Requisitos
Python 3.10+

KeyDB (local o remoto)

Pip para instalar dependencias

Navegador web

🛠 Instalación de KeyDB (local)
Windows
Descargar KeyDB desde la página oficial.

Descomprimir y ejecutar keydb-server.exe.

Por defecto, KeyDB escucha en el puerto 6379. Puedes cambiarlo si deseas.

## Funcionalidades
**Agregar libro:** Formulario web para registrar título, autor, género y estado (pendiente, leyendo, leído).

**Actualizar libro:** Editar información de un libro existente.

**Eliminar libro:** Eliminar un libro de la base de datos.

**Listar libros:** Mostrar todos los libros registrados.

**Buscar libros:** Filtrar libros por título, autor o género.

## Estructura de datos (JSON)
Cada libro se almacena en KeyDB como un documento JSON:

json
Copiar
Editar
{
  "id": "uuid-unico",
  "titulo": "Nombre del libro",
  "autor": "Nombre del autor",
  "genero": "Categoría",
  "estado": "pendiente/leyendo/leído"
}

## Validaciones y manejo de errores
Campos obligatorios: título, autor, género, estado.

Estado de lectura: solo pendiente, leyendo o leído.

Duplicados: se permite el mismo libro varias veces (no se considera error).

Conexión KeyDB: si falla, la aplicación no se inicia.

Búsquedas sin resultados muestran mensaje informativo.
