# Biblioteca Web con Flask y KeyDB

Aplicación web para gestionar una biblioteca personal usando Flask como framework web y KeyDB como almacenamiento en memoria. Permite agregar, actualizar, eliminar, listar y buscar libros mediante una interfaz web.

## Requisitos
Python 3.10+

KeyDB (local o remoto)

Pip para instalar dependencias

Navegador web

## Instalación de KeyDB con Docker
Descargar e instalar Docker Desktop: https://www.docker.com/products/docker-desktop

Ejecutar KeyDB en un contenedor:

buscar en images key db
![ky](https://github.com/user-attachments/assets/10db0bbd-eb1b-408b-9a6f-7c8f96f62345)


lo instalas, haces la configuracion basica y lo corres en un contenedor

Verificar que el contenedor esté corriendo: puedes verificar en con el codigo haciendo esto
![pn](https://github.com/user-attachments/assets/bd02d1f1-3972-450f-9195-dca81ca6667f)


## Funcionalidades
**Agregar libro:** Formulario web para registrar título, autor, género y estado (pendiente, leyendo, leído).

**Actualizar libro:** Editar información de un libro existente.

**Eliminar libro:** Eliminar un libro de la base de datos.

**Listar libros:** Mostrar todos los libros registrados.

**Buscar libros:** Filtrar libros por título, autor o género.

## Estructura de datos (JSON)
Cada libro se almacena en KeyDB como un documento JSON:

json

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
