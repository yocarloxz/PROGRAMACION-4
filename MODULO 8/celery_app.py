from celery import Celery
from flask import Flask
from flask_mail import Mail
import config

# ---- Flask app ----
app = Flask(__name__)
app.secret_key = "supersecreto"

# Configuración de Flask-Mail
app.config.update(
    MAIL_SERVER=getattr(config, "MAIL_SERVER", "smtp.gmail.com"),
    MAIL_PORT=getattr(config, "MAIL_PORT", 587),
    MAIL_USE_TLS=getattr(config, "MAIL_USE_TLS", True),
    MAIL_USE_SSL=getattr(config, "MAIL_USE_SSL", False),
    MAIL_USERNAME=getattr(config, "MAIL_USERNAME", None),
    MAIL_PASSWORD=getattr(config, "MAIL_PASSWORD", None),
    MAIL_DEFAULT_SENDER=getattr(config, "MAIL_DEFAULT_SENDER", None)
)
mail = Mail(app)

# ---- Celery app ----
celery = Celery(
    "tasks",
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0",
    backend=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/0"
)

# Permite que las tareas accedan al contexto de Flask
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
