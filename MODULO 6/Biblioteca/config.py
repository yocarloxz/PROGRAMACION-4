import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6060))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

try:
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    client.ping()
    print("Conectado a KeyDB")
except redis.ConnectionError:
    print("No se pudo conectar a KeyDB.")
    exit(1)
