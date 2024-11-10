# config.py

import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()


class Config:
    # Base settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    ENTRA_ID_TENANT_ID = os.getenv("ENTRA_ID_TENANT_ID", "default_tenant_id")

    # Database configuration
    DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+aiomysql://todo_user:todo_pass@localhost:3306/cbc_todo"
    )

    # Redis configuration
    REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379/0")

    # Azure Storage Queue URI (si vous en avez besoin)
    AZURE_STORAGE_QUEUE_URI = os.getenv(
        "AZURE_STORAGE_QUEUE_URI", "http://localhost:10001/devstoreaccount1"
    )

    # Sanic specific settings
    SANIC_DEBUG = os.getenv("SANIC_DEBUG", "False") == "True"
    SANIC_AUTO_RELOAD = os.getenv("SANIC_AUTO_RELOAD", "True") == "True"
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "http://localhost:3000")


# Vous pouvez ajouter d'autres paramètres globaux ici comme les queues Azure, etc.
