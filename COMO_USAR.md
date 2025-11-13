# 🚀 Guía Rápida: Cómo Transcribir Audio

## Paso 1: Iniciar el Servidor
1. Abre PyCharm
2. Ve al archivo `main.py`
3. Haz clic en el botón **Play (▶️)** en la esquina superior derecha
4. Espera a que aparezca: `INFO: Uvicorn running on http://127.0.0.1:8000`

## Paso 2: Probar que Funciona
Ejecuta el script de prueba:
```bash
python test_server.py
```

## Paso 3: Transcribir tu Audio

### Opción A: Desde Python
```python
import requests

# Tu archivo de audio
response = requests.post('http://127.0.0.1:8000/api/transcribe', json={
    'file_path': 'C:\\Users\\HALO\\Desktop\\mi_audio.mp3',  # ← Cambia esta ruta
    'language': 'es'  # 'es', 'en', 'fr', etc.
})

texto = response.json()['text']
print(texto)
```

### Opción B: Desde JavaScript (NestJS)
```javascript
const axios = require('axios');

const response = await axios.post('http://127.0.0.1:8000/api/transcribe', {
    file_path: '/path/to/your/audio.mp3',  // ← Cambia esta ruta
    language: 'es'
});

console.log(response.data.text);
```

### Opción C: Desde cURL
```bash
curl -X POST "http://127.0.0.1:8000/api/transcribe" \
     -H "Content-Type: application/json" \
     -d '{"file_path": "C:\\Users\\HALO\\Desktop\\mi_audio.mp3", "language": "es"}'
```

### Opción D: Usando el archivo test_main.http
1. Abre `test_main.http` en PyCharm
2. Modifica la ruta del archivo en el JSON
3. Haz clic en "Run" junto a la solicitud

## 📁 Dónde Colocar tus Archivos de Audio

- **Ruta absoluta**: `C:\Users\HALO\Desktop\audio.mp3`
- **Ruta relativa**: `./test_audio/audio.mp3`
- **Carpeta del proyecto**: `test_audio/mi_audio.wav`

## 🎵 Formatos Soportados
- MP3, WAV, M4A, FLAC, OGG y más...

## 🌐 Idiomas
- `es` (Español), `en` (Inglés), `fr` (Francés), etc.

## ⚡ Consejos
- La primera transcripción tarda más (carga el modelo)
- Asegúrate de que el archivo existe en la ruta especificada
- El servidor debe estar ejecutándose

¡Listo! Tu servidor de Whisper está funcionando. 🎉
