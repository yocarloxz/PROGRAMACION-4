# Biblioteca KeyDB

## Descripción
Esta aplicación de línea de comandos permite gestionar una biblioteca personal utilizando KeyDB, un sistema de almacenamiento en memoria compatible con Redis. Cada libro se guarda como un objeto JSON y las operaciones CRUD se realizan mediante la biblioteca redis-py.

## Requisitos
Python 3.11 o superior

Docker (para ejecutar KeyDB en contenedor)

Paquetes Python: redis, python-dotenv

## Instalación de KeyDB con Docker
Descargar e instalar Docker Desktop: https://www.docker.com/products/docker-desktop

Ejecutar KeyDB en un contenedor:

buscar en images key db
![ky](https://github.com/user-attachments/assets/10db0bbd-eb1b-408b-9a6f-7c8f96f62345)
lo instalas, haces la configuracion basica y lo corres en un contenedor

Verificar que el contenedor esté corriendo: puedes verificar en con el codigo haciendo esto
![pn](https://github.com/user-attachments/assets/bd02d1f1-3972-450f-9195-dca81ca6667f)

Crear un archivo .env en la raíz del proyecto con la configuración de KeyDB:

REDIS_HOST=localhost
REDIS_PORT=6379(default)
REDIS_PASSWORD=
Si tu KeyDB tiene contraseña, colócala en REDIS_PASSWORD.

Ejecutar la aplicación

## Operaciones disponibles

Agregar libro: Título, autor, género y estado (pendiente, leyendo, leído).

Actualizar libro: Permite modificar campos dejando en blanco los que no se cambian.

Eliminar libro: Elimina un libro usando su ID.

Listar libros: Muestra todos los libros registrados.

Buscar libros: Busca por título, autor o género.

Salir: Termina la aplicación.


## Manejo de errores
Conexión fallida: Si KeyDB no está activo o la configuración es incorrecta, el programa termina mostrando un mensaje de error.

Libro no encontrado: Al actualizar, eliminar o buscar, si la clave no existe se notifica al usuario.

Campos vacíos: El programa obliga a completar todos los campos al agregar un libro.

Estado inválido: Solo se permiten pendiente, leyendo o leído como valores válidos para el estado de lectura.
