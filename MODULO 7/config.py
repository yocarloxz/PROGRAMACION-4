import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6060))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

