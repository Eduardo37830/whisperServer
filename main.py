"""
Servidor FastAPI para transcripción de audio con Whisper
Estructura modular y limpia
"""
import logging
import uvicorn
from fastapi import FastAPI

from config import WHISPER_MODEL, HOST, PORT, DEBUG
from services import WhisperService
from routes import router, set_whisper_service

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- 1. Inicializa la app de FastAPI ---
app = FastAPI(
    title="Servidor de Transcripción Whisper",
    description="API para transcribir archivos de audio usando OpenAI Whisper",
    version="1.0.0"
)

# --- 2. Carga el modelo de Whisper al iniciar ---
@app.on_event("startup")
async def startup_event():
    """Ejecuta al iniciar la aplicación"""
    logger.info("Iniciando servidor...")
    whisper_service = WhisperService(model_name=WHISPER_MODEL)
    set_whisper_service(whisper_service)
    logger.info("Servidor iniciado correctamente")


# --- 3. Incluir rutas ---
app.include_router(router)


if __name__ == "__main__":
    logger.info(f"Iniciando servidor en {HOST}:{PORT}")
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info" if DEBUG else "warning"
    )
