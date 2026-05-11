import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / '.env')
load_dotenv(BASE_DIR.parent / '.env.example', override=False)

class Settings:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    ADMIN_CHAT_ID: str = os.getenv('ADMIN_CHAT_ID', '')
    BACKEND_API_URL: str = os.getenv('BACKEND_API_URL', 'http://backend:8000/api/')

settings = Settings()
