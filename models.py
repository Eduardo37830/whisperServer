"""
Modelos de datos (Pydantic) para la API
"""
from pydantic import BaseModel, Field


class AudioRequest(BaseModel):
    """Solicitud de transcripción de audio"""
    file_path: str = Field(..., description="Ruta al archivo de audio")
    language: str = Field(default="es", description="Código de idioma (ej: es, en, fr)")

    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "/path/to/audio.mp3",
                "language": "es"
            }
        }


class TranscriptionResponse(BaseModel):
    """Respuesta de transcripción"""
    text: str = Field(..., description="Texto transcrito")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hola, esto es una prueba de transcripción."
            }
        }


class StatusResponse(BaseModel):
    """Respuesta de estado del servidor"""
    status: str = Field(..., description="Estado del servidor")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "Servidor de Whisper local está activo"
            }
        }

