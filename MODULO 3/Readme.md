# Biblioteca Personal - Gestión con MariaDB y SQLAlchemy

## Descripción
Este proyecto es una aplicación de línea de comandos en Python para administrar una biblioteca personal.  
Permite agregar, actualizar, eliminar, listar y buscar libros almacenados en una base de datos MariaDB utilizando SQLAlchemy como ORM.


## Requisitos

- Python 3.8 o superior  
- MariaDB instalado y corriendo en Windows 10  
- Paquetes Python:
  - SQLAlchemy
  - PyMySQL


## Instalación

1. **Instalar MariaDB en Windows 10**

   - Descarga el instalador desde [https://mariadb.org/download/](https://mariadb.org/download/)  
   - Sigue las instrucciones para la instalación.  
   - Durante la instalación, configura usuario, contraseña y puerto (por defecto 3306).

2. **Crear la base de datos**

   - Abre HeidiSQL o cliente de MariaDB.  
   - Ejecuta el siguiente comando para crear la base de datos:

     CREATE DATABASE biblioteca;

  - En HeidiSQL despues de configurarlo y añadir la conexion puedes crear la base de datos con click derecho en el espacio de la izquierda:
  - crear nueva -> base de datos, despues dandole doble click puedes ver los datos que ya añadiste a la tabla dandole click a pestaña que dice datos en la base de datos

3. **Instalar dependencias**

   SQLAlchemy
   pymysq
