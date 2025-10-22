# Jarvis (Qwen2.5-3B-Instruct Q4, vía Ollama) — Windows

Agente local minimalista que **ejecuta órdenes en tu PC** con lenguaje natural.
- **Backend único**: Ollama + **qwen2.5:3b-instruct-q4_0** (no usa otros modelos).
- **Planner** ReAct simple (máx. 5 pasos).
- **Herramientas**: `filesystem` (leer/escribir/listar) y `shell` (PowerShell con confirmación).
- **Interfaces**: CLI (`python -m jarvis`) y API (FastAPI).

---

## Instalación (Windows 10/11)

1) **Ollama** instalado y ejecutándose.  
   Descarga: https://ollama.com/download

2) **Pull del modelo** (único soportado por defecto):
```ps1
ollama pull qwen2.5:3b-instruct-q4_0
```

3) **Python 3.10+** y dependencias:
```ps1
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Uso

### CLI
```ps1
python -m jarvis "crea un archivo 'nota.txt' con el texto 'hola mundo' en el Escritorio"
```

### API
```ps1
uvicorn jarvis.server:app --host 127.0.0.1 --port 8000
```
Ejemplo:
```http
POST http://127.0.0.1:8000/ask
{ "input": "lista los archivos de C:\\Users\\TUUSUARIO\\Desktop" }
```

---

## Seguridad
- **Rutas seguras**: Escritorio del usuario y carpeta del proyecto.
- **shell.run**: Confirmación para comandos peligrosos (del, rm, rmdir, shutdown, etc.).

---

## Extensión
Añade nuevas herramientas en `jarvis/tools/` y regístralas en `tools/__init__.py`.

---

## Problemas comunes
- **Error 11434**: inicia Ollama (`ollama serve`) y asegúrate de haber hecho *pull* del modelo.  
- **Permisos PowerShell**: abre PowerShell 7 (pwsh) o como Administrador si hay políticas restrictivas.
