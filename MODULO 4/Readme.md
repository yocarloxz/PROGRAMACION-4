# 📚 Biblioteca Personal con MongoDB y PyMongo

Aplicación de línea de comandos para gestionar una biblioteca personal utilizando **MongoDB** como base de datos no relacional y **PyMongo** como cliente de conexión.

El sistema permite:
- 📥 Agregar libros
- ✏ Actualizar libros
- 🗑 Eliminar libros
- 📜 Listar todos los libros
- 🔍 Buscar libros por título, autor o género
- 🚪 Salir del programa

---

## 📌 Requisitos previos

Antes de usar esta aplicación, debes tener:

- **Python 3.8 o superior** instalado.
- **pip** (administrador de paquetes de Python) actualizado.
- **MongoDB** instalado localmente o acceso a **MongoDB Atlas**.
- **Conexión a internet** si usas MongoDB Atlas.

---

## 🛠 Instalación de MongoDB

### 🔹 Opción 1: Instalación local (recomendada para desarrollo)
1. Descarga MongoDB Community Server desde:  
   👉 [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Durante la instalación, selecciona **"Run MongoDB as a Service"** para que se ejecute automáticamente.
3. (Opcional) Instala **MongoDB Compass** para gestionar la base de datos visualmente:  
   👉 [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
4. Para iniciar el servicio manualmente en Windows:
   ```powershell
   net start MongoDB
