"""
Configuración de la aplicación
"""
import os

# Configuración del modelo Whisper
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "es")

# Configuración del servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

