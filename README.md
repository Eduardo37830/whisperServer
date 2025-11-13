# whisperlocal — Servidor FastAPI modular para Whisper

Proyecto modular que expone un endpoint REST para transcribir audios usando **OpenAI Whisper** (modelo local).

---

## 📁 Estructura del proyecto

* `main.py`: Punto de entrada de la aplicación, configura FastAPI y la startup.
* `config.py`: Variables de configuración centralizadas (modelo, puerto, idioma, etc.).
* `models.py`: Modelos Pydantic para validación de entrada/salida.
* `services.py`: Lógica de negocio (`WhisperService`) separada de las rutas.
* `routes.py`: Definición de endpoints de la API.
* `GPU.md`: Guía opcional para configurar Whisper con GPU (CUDA).

---

## ✅ Ventajas de esta estructura modular

* Separación clara de responsabilidades.
* Código más fácil de mantener y escalar.
* Pruebas unitarias más simples.
* Configuración centralizada.
* Mejor legibilidad del código.
* Posible reutilización de `WhisperService` en otros proyectos.

---

## 🚀 Requisitos (rápido)

Desde el entorno virtual del proyecto (`.venv`), instala:

```bash
pip install openai-whisper pydantic fastapi uvicorn
```

Si planeas usar GPU, revisa el archivo `GPU.md`.

---

## ⚙️ Variables de entorno

Puedes personalizar el comportamiento del servidor mediante variables de entorno:

* `WHISPER_MODEL` — Modelo a usar (`tiny`, `base`, `small`, `medium`, `large`).
  **Default:** `base`
* `WHISPER_DEVICE` — Dispositivo (`cpu` o `cuda`).
  **Default:** `cpu`
* `DEFAULT_LANGUAGE` — Idioma por defecto (código tipo `es`, `en`, etc.).
  **Default:** `es`
* `HOST` — Host para uvicorn.
  **Default:** `0.0.0.0`
* `PORT` — Puerto HTTP del servidor.
  **Default:** `8000`
* `DEBUG` — Modo debug (`True`/`False`).
  **Default:** `False`

### Ejemplo en Linux/Mac (bash)

```bash
export WHISPER_MODEL=base
export WHISPER_DEVICE=cpu
export DEFAULT_LANGUAGE=es
export HOST=0.0.0.0
export PORT=8000
export DEBUG=False
```

### Ejemplo en Windows (cmd.exe)

```cmd
set WHISPER_MODEL=base
set WHISPER_DEVICE=cpu
set DEFAULT_LANGUAGE=es
set HOST=0.0.0.0
set PORT=8000
set DEBUG=False
```

---

## 🧠 Elegir el modelo de Whisper según tu PC

Whisper incluye varios tamaños de modelo. La idea general:

* Mientras **más pequeño** es el modelo → **menos recursos** consume y **más rápido** es, pero puede ser **menos preciso**.
* Mientras **más grande** es el modelo → **más RAM/VRAM** necesita y **es más lento**, pero mejora la **calidad de la transcripción**.

### Modelos más usados en `openai-whisper`

| Modelo   | Calidad aprox. | Velocidad      | RAM/VRAM recomendada | Uso recomendado                                      |
| -------- | -------------- | -------------- | -------------------- | ---------------------------------------------------- |
| `tiny`   | Básica         | 🚀 Muy alta    | ≥ 2 GB               | PCs muy modestas, pruebas rápidas, audios cortos     |
| `base`   | Mejor que tiny | 🚀 Alta        | ≥ 4 GB               | Buen punto de inicio en la mayoría de PCs            |
| `small`  | Buena          | ⚖️ Media       | ≥ 6–8 GB             | Mejor calidad, si tu PC aguanta                      |
| `medium` | Muy buena      | 🐢 Lenta       | ≥ 8–12 GB            | Equipos con buena CPU o GPU, proyectos más exigentes |
| `large`  | Excelente      | 🐢🐢 Más lenta | ≥ 12–16 GB           | Servidores potentes / GPU dedicada, máxima calidad   |

> También existen variantes como `tiny.en`, `base.en`, `small.en`, `medium.en` optimizadas solo para inglés.
> Para este proyecto en español normalmente usaremos los modelos **sin** `.en`.

### Recomendaciones rápidas para tus compañeros

1. 💻 **Portátil básico (4 GB RAM, sin GPU potente)**

   * Usa: `tiny` o `base`
   * Ejemplo:

     ```cmd
     set WHISPER_MODEL=base
     ```

2. 💻 **PC de escritorio media (8 GB RAM, CPU decente)**

   * Usa: `base` o `small`
   * Ejemplo:

     ```cmd
     set WHISPER_MODEL=small
     ```

3. 🖥️ **PC/GPU potente (RTX, 8–12+ GB de VRAM)**

   * Usa: `small`, `medium` o incluso `large`
   * Ejemplo:

     ```cmd
     set WHISPER_MODEL=medium
     set WHISPER_DEVICE=cuda
     ```

---

## ▶️ Cómo ejecutar el servidor

Puedes ejecutarlo de dos formas:

### Desde PyCharm

1. Abre el proyecto en PyCharm.
2. Asegúrate de que el intérprete apunte a tu entorno virtual (si usas `.venv`).
3. Abre `main.py`.
4. Haz clic en el botón **Play (▶️)** para ejecutar.

### Desde la terminal

En la raíz del proyecto:

```bash
python main.py
```

Por defecto, el servidor quedará disponible en:

```text
http://127.0.0.1:8000
```

> Si inicias con `HOST=0.0.0.0`, deberás usar la IP del servidor para acceder desde otros equipos de la red.

---

## 🎯 Endpoint principal: `/api/transcribe`

* **Método:** `POST`
* **URL:** `http://127.0.0.1:8000/api/transcribe`
* **Content-Type:** `application/json`

### Body (JSON)

* `file_path` (string, requerido) — Ruta completa al archivo de audio **en el sistema de archivos del servidor**.
* `language` (string, opcional) — Código de idioma (`es`, `en`, `fr`, etc.). Si no se envía, se usa `DEFAULT_LANGUAGE`.

Ejemplo (Windows, JSON):

```json
{
  "file_path": "C:\\\\Users\\\\HALO\\\\Downloads\\\\IRIS OUT - Chainsaw Man - The Movie_ Reze Arc (Spanish Cover by Tricker).mp3",
  "language": "es"
}
```

> Nota: en JSON las barras invertidas (`\`) deben ir escapadas (`\\`).

### Respuesta exitosa (ejemplo)

```json
{
  "text": "Hola, este es el texto transcrito del audio."
}
```

---

## 📝 Parámetros

| Parámetro   | Tipo   | Requerido | Descripción                            |
| ----------- | ------ | --------- | -------------------------------------- |
| `file_path` | string | ✅         | Ruta completa al archivo de audio      |
| `language`  | string | ❌         | Código de idioma (por defecto: `"es"`) |

---

## 🎵 Formatos de audio soportados

Whisper soporta múltiples formatos, entre ellos:

* MP3 (`.mp3`)
* WAV (`.wav`)
* M4A (`.m4a`)
* FLAC (`.flac`)
* OGG (`.ogg`)
* Y muchos más…

---

## 🌐 Idiomas soportados

Whisper soporta un gran número de idiomas. Algunos comunes:

* `es` — Español
* `en` — Inglés
* `fr` — Francés
* `de` — Alemán
* `it` — Italiano
* `pt` — Portugués
* `ja` — Japonés
* `zh` — Chino

(…y otros muchos códigos estándar ISO 639-1).

---

## 🚀 Cómo transcribir un audio (paso a paso)

1. Asegúrate de que el servidor esté ejecutándose (`main.py` en marcha).
2. Verifica que el archivo de audio exista en la ruta indicada.
3. Envía una petición `POST` al endpoint `/api/transcribe` con el JSON correcto.
4. Revisa la respuesta JSON: el campo `text` contiene la transcripción.

---

## 💻 Ejemplos prácticos de consumo

### Desde Python

```python
import requests

payload = {
    "file_path": r"C:\\Users\\HALO\\Desktop\\audio.mp3",
    "language": "es"
}

response = requests.post(
    "http://127.0.0.1:8000/api/transcribe",
    json=payload
)

data = response.json()
print("Texto transcrito:", data["text"])
```

### Desde cURL (Linux/Mac)

```bash
curl -X POST "http://127.0.0.1:8000/api/transcribe" \
     -H "Content-Type: application/json" \
     -d '{"file_path": "/ruta/completa/al/archivo.mp3", "language": "es"}'
```

### Desde cURL (Windows cmd)

```cmd
curl -X POST "http://127.0.0.1:8000/api/transcribe" ^
     -H "Content-Type: application/json" ^
     -d "{\"file_path\": \"C:\\\\Users\\\\HALO\\\\Desktop\\\\audio.mp3\", \"language\": \"es\"}"
```

---

## 🛠️ Depuración de errores comunes

* **HTTP 422 Unprocessable Entity**
  El JSON enviado no coincide con el modelo esperado.

  * Asegúrate de enviar `file_path` (y opcionalmente `language`) en el body.
  * Verifica que el `Content-Type` sea `application/json`.
  * Revisa comillas y comas en el JSON.

* **“Archivo no encontrado” / errores de ruta**

  * Verifica que la ruta exista y sea accesible desde el servidor.
  * En Windows, revisa bien las barras invertidas y los permisos.

* **`FP16 is not supported on CPU`**

  * Mensaje informativo: cuando Whisper intenta usar fp16 en CPU.
  * No suele ser crítico: el modelo se ejecuta en fp32 automáticamente.

* **Problemas de memoria (OOM)**

  * Prueba con un modelo más pequeño (`base` o `tiny`).
  * Cierra otros programas que consuman mucha RAM/VRAM.

---

## ⚡ Uso de GPU (opcional)

Si quieres usar Whisper con GPU (por ejemplo, una RTX):

1. Instala PyTorch con soporte CUDA (consulta la guía oficial según tu versión de CUDA).

2. Configura la variable de entorno:

   ```bash
   export WHISPER_DEVICE=cuda
   # o en Windows:
   # set WHISPER_DEVICE=cuda
   ```

3. Elige un modelo acorde a tu VRAM (`small`, `medium` o `large`).

4. Revisa el archivo `GPU.md` incluido en el proyecto para una guía paso a paso.

---

## 📚 Archivos útiles

* `main.py` — Punto de entrada del servidor FastAPI.
* `config.py` — Configuración centralizada (modelo, device, idioma, puerto…).
* `models.py` — Esquemas Pydantic para request/response.
* `services.py` — Lógica principal de transcripción (`WhisperService`).
* `routes.py` — Rutas y endpoints de la API.
* `GPU.md` — Guía para habilitar GPU/CUDA.

---
 
 
