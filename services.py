"""
Servicio de transcripción con Whisper
"""
import os
import logging
from typing import Optional

try:
    import whisper
except ImportError:
    whisper = None

logger = logging.getLogger(__name__)


class WhisperService:
    """Servicio para manejar la transcripción de audio con Whisper"""

    def __init__(self, model_name: str = "base"):
        """
        Inicializa el servicio de Whisper

        Args:
            model_name: Nombre del modelo ("tiny", "base", "small", "medium", "large")
        """
        self.model_name = model_name
        self.model: Optional[object] = None
        self._load_model()

    def _load_model(self) -> None:
        """Carga el modelo de Whisper"""
        if not whisper:
            logger.error("whisper no está instalado")
            return

        try:
            logger.info(f"Cargando modelo de Whisper: '{self.model_name}'...")
            self.model = whisper.load_model(self.model_name)
            logger.info(f"Modelo '{self.model_name}' cargado exitosamente.")
        except Exception as e:
            logger.error(f"Error cargando el modelo: {e}")
            self.model = None

    def is_ready(self) -> bool:
        """Verifica si el modelo está listo para usar"""
        return self.model is not None

    def transcribe(self, file_path: str, language: str = "es") -> str:
        """
        Transcribe un archivo de audio

        Args:
            file_path: Ruta al archivo de audio
            language: Código de idioma

        Returns:
            Texto transcrito

        Raises:
            ValueError: Si el modelo no está cargado o el archivo no existe
        """
        if not self.is_ready():
            raise ValueError("El modelo de Whisper no está cargado")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        try:
            logger.info(f"Procesando archivo: {file_path}")
            result = self.model.transcribe(file_path, language=language)  # type: ignore
            logger.info("Transcripción completada")
            return result["text"]
        except Exception as e:
            logger.error(f"Error en la transcripción: {e}")
            raise

