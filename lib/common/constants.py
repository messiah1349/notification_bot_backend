import os

TZ = os.getenv('TZ', 'Europe/Helsinki')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
API_TOKEN = os.getenv('NOTIFICATION_BOT_TOKEN', '214139458:AAH8UGU0PW3vUE1lRz-gjXnlB6TroUvpfUk')