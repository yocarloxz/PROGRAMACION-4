import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:5001")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecreto")
