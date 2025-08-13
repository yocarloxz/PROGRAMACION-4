from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cambia los datos de conexión según tu configuración local
DB_USER = 'usuario'
DB_PASSWORD = 'contraseña'
DB_HOST = 'localhost'
DB_NAME = 'nombre de la base de datos'

# Cadena de conexión para MariaDB
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Crear el engine
engine = create_engine(DATABASE_URL, echo=False)

# Crear sesión
SessionLocal = sessionmaker(bind=engine)
