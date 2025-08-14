from flask import Flask
from flask_mail import Mail
import redis
import config

# Flask app
app = Flask(__name__)
app.secret_key = "supersecreto"

# Flask-Mail
mail = Mail(app)
app.config.update(
    MAIL_SERVER=getattr(config, "MAIL_SERVER", ""),
    MAIL_PORT=getattr(config, "MAIL_PORT", 587),
    MAIL_USERNAME=getattr(config, "MAIL_USERNAME", ""),
    MAIL_PASSWORD=getattr(config, "MAIL_PASSWORD", ""),
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER=getattr(config, "MAIL_DEFAULT_SENDER", "")
)

# KeyDB / Redis
client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=True
)
