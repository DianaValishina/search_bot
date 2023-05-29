from os import environ
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Bot configurations
API_TOKEN = environ["API_TOKEN"]
WEBAPP_HOST = environ["WEBAPP_HOST"]
WEBAPP_PORT = int(environ["WEBAPP_PORT"])
DEBUG = environ["DEBUG"].lower() == "true"

# Webhook configurartion
WEBHOOK_HOST = environ["WEBHOOK_HOST"]
WEBHOOK_PATH = environ["WEBHOOK_PATH"]
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


# Redis connection configuration
REDIS_STORAGE_HOST = environ["REDIS_HOST"]
REDIS_STORAGE_PORT = int(environ["REDIS_PORT"])
REDIS_STORAGE_DB = int(environ["REDIS_DB"])
