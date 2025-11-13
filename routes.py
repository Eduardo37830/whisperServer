"""
Rutas (endpoints) de la API
"""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException

from models import AudioRequest, TranscriptionResponse, StatusResponse
from services import WhisperService

logger = logging.getLogger(__name__)
router = APIRouter()

# Instancia del servicio (será inyectado desde main.py)
whisper_service: Optional[WhisperService] = None


def set_whisper_service(service: WhisperService) -> None:
    """Inyecta la instancia del servicio de Whisper"""
    global whisper_service
    whisper_service = service


@router.get("/", response_model=StatusResponse)
def read_root():
    """Endpoint raíz para verificar que el servidor está activo"""
    return {"status": "Servidor de Whisper local está activo"}


@router.post("/api/transcribe", response_model=TranscriptionResponse)
def transcribe_audio(request: AudioRequest):
    """
    Transcribe un archivo de audio

    Args:
        request: Datos de solicitud con ruta del archivo y idioma

    Returns:
        Texto transcrito
    """
    if not whisper_service or not whisper_service.is_ready():
        raise HTTPException(
            status_code=500,
            detail="El modelo de Whisper no está cargado"
        )

    try:
        text = whisper_service.transcribe(
            request.file_path,
            language=request.language
        )
        return {"text": text}
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error en transcripción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

