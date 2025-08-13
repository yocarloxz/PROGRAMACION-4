Biblioteca Personal con MongoDB y PyMongo
Aplicación de línea de comandos para gestionar una biblioteca personal utilizando MongoDB como base de datos no relacional y PyMongo como cliente de conexión.

El sistema permite:

Agregar libros
Actualizar libros
Eliminar libros
Listar todos los libros
Buscar libros por título, autor o género
Salir del programa
Requisitos previos
Antes de usar esta aplicación, debes tener:

Python 3.8 o superior instalado.
pip (administrador de paquetes de Python) actualizado.
MongoDB instalado localmente o acceso a MongoDB Atlas.
Conexión a internet si usas MongoDB Atlas.
Instalación de MongoDB
Opción 1: Instalación local (recomendada para desarrollo)
Descarga MongoDB Community Server desde:
https://www.mongodb.com/try/download/community

Durante la instalación, selecciona "Run MongoDB as a Service" para que se ejecute automáticamente.

(Opcional) Instala MongoDB Compass para gestionar la base de datos visualmente:
https://www.mongodb.com/try/download/compass

Para iniciar el servicio manualmente en Windows:

net start MongoDB

Y para detenerlo:

net stop MongoDB

Validaciones incluidas Error de conexión: Si MongoDB no está disponible, el programa muestra un mensaje y se detiene.

Documentos mal estructurados: El sistema valida que todos los campos requeridos estén presentes.

Búsquedas sin resultados: Si no se encuentran libros, se informa al usuario.
