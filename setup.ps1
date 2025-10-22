Write-Host "=== Jarvis (Qwen2.5-3B Q4) Setup ==="
Write-Host "1) Pull del modelo único (qwen2.5:3b-instruct-q4_0) en Ollama..."
ollama pull qwen2.5:3b-instruct-q4_0
Write-Host "2) Creando entorno virtual..."
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
Write-Host "3) Instalando dependencias..."
pip install -r requirements.txt
Write-Host "Listo. Ejecuta el agente con:  python -m jarvis --help"
