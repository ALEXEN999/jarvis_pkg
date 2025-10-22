# Jarvis — Agente local (Qwen 3B, Ollama)
![CI Status](https://img.shields.io/github/actions/workflow/status/ALEXEN999/jarvis/python-ci.yml?branch=main&label=CI)
![Tests](https://img.shields.io/github/actions/workflow/status/ALEXEN999/jarvis/python-tests.yml?branch=main&label=Tests)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)

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
