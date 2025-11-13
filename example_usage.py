"""
Ejemplo de cómo usar el servidor de Whisper desde Python
"""
import requests
import json

def transcribe_audio(file_path: str, language: str = "es") -> str:
    """
    Transcribe un archivo de audio usando el servidor local de Whisper

    Args:
        file_path: Ruta completa al archivo de audio
        language: Código de idioma (ej: "es", "en", "fr")

    Returns:
        Texto transcrito

    Raises:
        Exception: Si hay error en la transcripción
    """
    url = "http://127.0.0.1:8000/api/transcribe"

    payload = {
        "file_path": file_path,
        "language": language
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza excepción si hay error HTTP

        result = response.json()
        return result["text"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error en la solicitud HTTP: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Error al procesar la respuesta: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Asegúrate de que el servidor esté ejecutándose primero

    # Ejemplo 1: Transcribir un archivo MP3
    try:
        texto = transcribe_audio("C:\\Users\\HALO\\Desktop\\mi_audio.mp3", "es")
        print(f"Transcripción: {texto}")
    except Exception as e:
        print(f"Error: {e}")

    # Ejemplo 2: Transcribir audio en inglés
    try:
        texto_en = transcribe_audio("./audio_files/english_audio.wav", "en")
        print(f"English transcription: {texto_en}")
    except Exception as e:
        print(f"Error: {e}")
