import os
from dotenv import load_dotenv

load_dotenv()

TZ = os.getenv('TZ', 'Europe/Helsinki')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
TELEGRAM_SENDER_HOST = os.getenv('TELEGRAM_SENDER_HOST', 'localhost')
TELEGRAM_SENDER_PORT = os.getenv('TELEGRAM_SENDER_PORT', '8002')
API_TOKEN = os.getenv('NOTIFICATION_BOT_TOKEN', '')
