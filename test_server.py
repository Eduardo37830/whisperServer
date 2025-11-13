"""
Script para probar el servidor de Whisper
Ejecuta este archivo para verificar que todo funciona correctamente
"""
import requests
import os
import sys

def test_server_status():
    """Prueba que el servidor esté funcionando"""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            return True
        else:
            print(f"❌ Error en el servidor: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose?")
        print("   Ejecuta main.py primero desde PyCharm")
        return False

def test_transcription(file_path: str, language: str = "es"):
    """Prueba la transcripción de un archivo"""
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        print("   Coloca un archivo de audio en la ruta especificada")
        return False

    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/transcribe",
            json={"file_path": file_path, "language": language}
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Transcripción exitosa!")
            print(f"📝 Texto: {result['text']}")
            return True
        else:
            error = response.json()
            print(f"❌ Error en transcripción: {error.get('detail', 'Error desconocido')}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧪 Probando servidor de Whisper local")
    print("=" * 50)

    # 1. Verificar que el servidor esté funcionando
    if not test_server_status():
        sys.exit(1)

    print()

    # 2. Intentar transcribir un archivo de prueba
    print("🎵 Probando transcripción...")

    # Buscar archivos de audio en la carpeta test_audio
    test_dir = "test_audio"
    audio_files = []

    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            if file.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
                audio_files.append(os.path.join(test_dir, file))

    if audio_files:
        print(f"📁 Encontrados {len(audio_files)} archivos de audio en {test_dir}")
        for audio_file in audio_files[:1]:  # Solo probar el primero
            print(f"🎧 Probando con: {audio_file}")
            test_transcription(audio_file)
            break
    else:
        print("📁 No se encontraron archivos de audio en la carpeta 'test_audio'")
        print("💡 Para probar:")
        print("   1. Coloca un archivo de audio en la carpeta 'test_audio'")
        print("   2. O modifica este script para usar una ruta específica")
        print()
        print("   Ejemplo de uso manual:")
        print("   test_transcription('C:\\\\Users\\\\HALO\\\\Desktop\\\\audio.mp3')")

if __name__ == "__main__":
    main()
