# GPU.md — Usar la RTX con Whisper en Windows

Esta guía te explica cómo preparar Windows para que Whisper (a través de PyTorch) use tu GPU NVIDIA RTX.

1) Comprobar que Windows detecta la GPU
- Abre PowerShell o cmd.exe y ejecuta:

```cmd
nvidia-smi
```

Si no está instalado o no funciona, instala/actualiza los drivers NVIDIA desde: https://www.nvidia.com/Download/index.aspx

2) Instalar PyTorch con soporte CUDA
- Ve a https://pytorch.org/get-started/locally/ y selecciona la versión de CUDA que quieras (p. ej. cu121 para CUDA 12.1).
- Ejemplo (PowerShell / cmd):

```cmd
pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio --upgrade
```

Reemplaza `cu121` por la versión que corresponda a tu entorno (p. ej. `cu118`, `cu117`, etc.).

3) Verificar en Python

```cmd
python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA version:', torch.version.cuda if torch.cuda.is_available() else 'N/A')"
```

Resultado esperado: `CUDA available: True` y una versión de CUDA válida.

4) Configurar el servidor para usar `cuda`
- Exporta la variable de entorno (cmd.exe):

```cmd
set WHISPER_DEVICE=cuda
```

- Asegúrate en `config.py` o donde cargues el modelo que pasas el `device` correctamente a PyTorch. Un ejemplo sencillo cuando cargas el modelo:

```python
import whisper
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model('base')
model.to(device)
```

5) Notas y problemas comunes
- Si `torch.cuda.is_available()` es False:
  - Revisa `nvidia-smi` y que los drivers estén instalados.
  - Asegúrate de instalar la rueda de PyTorch con CUDA (no la versión CPU).
  - Reinicia el equipo si acabas de instalar drivers.

- WSL2: si trabajas dentro de WSL2 usa CUDA para WSL o instala los drivers compatibles.

- Memoria GPU: modelos grandes (ej.: `large`) pueden necesitar mucha VRAM; `base`/`small` son más moderados.

6) Prueba rápida desde el proyecto
- Inicia el servidor con `WHISPER_DEVICE=cuda` y revisa los logs; deberías ver que PyTorch detecta la GPU.

7) Recursos
- https://pytorch.org/
- https://developer.nvidia.com/cuda-downloads


Si quieres, puedo añadir al proyecto un script `check_gpu.py` que haga estas comprobaciones automáticamente y lo creo ahora mismo.
