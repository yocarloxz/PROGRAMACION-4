from flask import Flask
from .extensions import bootstrap, csrf, moment
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar extensiones
bootstrap.init_app(app)
csrf.init_app(app)
moment.init_app(app)
