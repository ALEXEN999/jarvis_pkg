# Jarvis — Agente local (Qwen 3B, Ollama)

Agente local que ejecuta acciones en tu PC (crear/leer/listar archivos y ejecutar comandos) con un modelo pequeño (Qwen 2.5 3B quantizado) para funcionar en GPUs de 8 GB de VRAM.

## Requisitos (Windows)
- Python 3.10+
- [Ollama](https://ollama.com/) instalado y corriendo
- Modelo: `qwen2.5:3b-instruct-q4_0` (descargar con `ollama pull qwen2.5:3b-instruct-q4_0`)
- PowerShell con permisos para scripts (o usar CLI Python sin scripts)

## Instalación
```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
