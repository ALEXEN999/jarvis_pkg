# Jarvis — Agente local (Qwen 3B, Ollama)
![CI](https://github.com/ALEXEN999/jarvis_pkg/actions/workflows/python-ci.yml/badge.svg?branch=main)
![Tests](https://github.com/ALEXEN999/jarvis_pkg/actions/workflows/python-tests.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/ALEXEN999/jarvis_pkg/branch/main/graph/badge.svg)](https://codecov.io/gh/ALEXEN999/jarvis_pkg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)

Agente local que ejecuta acciones en tu PC (crear/leer/listar archivos y ejecutar comandos) con un modelo pequeño (Qwen 2.5 3B quantizado) para funcionar en GPUs de 8 GB de VRAM.

## 🧠 Roadmap básico — Proyecto J.A.R.V.I.S. (Core → Asistente)
> **Propósito:** mantener una visión clara del desarrollo de JARVIS: qué hace, qué hará y cómo sabremos que cada etapa está completada.  
> **Ámbito actual:** Windows 10/11, modelo local (`qwen2.5:3b-instruct-q4_0`) con 8 GB VRAM, sin necesidad de Internet.

---

### ⚙️ Supuestos y contexto

- **Sistema operativo:** Windows 10/11  
- **Modelo por defecto:** Qwen 2.5 3B quantizado (Q4_0 – Ollama)  
- **Seguridad:** Solo actúa dentro de `SAFE_ROOTS` (Escritorio, OneDrive/Escritorio y carpeta del proyecto).  
- **Interfaz:** Línea de comandos (`python -m jarvis "<orden>"`)  
- **Privacidad:** Todo es local. Sin telemetría.

---

### 🧩 Fases del desarrollo

#### ✅ v1 — JARVIS Core estable (CLI, Windows)
**Objetivo:** ejecutar órdenes locales seguras en lenguaje natural.

**Funcionalidades**
- `filesystem.write`, `read`, `list`  
- `shell.run` con confirmación  
- Normalización de rutas (soporte “Escritorio” ↔ “Desktop”)  
- Seguridad de rutas (`SAFE_ROOTS`)  
- Parada automática tras ejecución exitosa  
- Trazas (TRACE) para depuración  

**Ejemplos**
- `python -m jarvis "crea un archivo 'nota.txt' con el texto 'Hola' en el Escritorio"`  
- `python -m jarvis "lee el archivo 'nota.txt' del Escritorio"`  
- `python -m jarvis "lista los archivos de mi Escritorio"`

---

#### 🗣️ v2 — Voz (hands-free)
**Objetivo:** hablar con JARVIS y escucharlo responder.

**Tareas**
- Voz → Texto (STT): `whisper.cpp` o `SpeechRecognition`  
- Texto → Voz (TTS): `edge-tts` o `pyttsx3`  
- Bucle de voz (`voice_loop.py`) con hotkey y baja latencia  

**Ejemplo:**  
> “Crea una nota que diga ‘Hola mundo’” → Jarvis la crea y responde con voz.

---

#### 💾 v3 — Memoria ligera + Configuración
**Objetivo:** recordar contexto y personalizar comportamiento.

**Tareas**
- Archivo `memory.json` (últimas N órdenes + resultados)  
- Archivo `config.json` o `.env` para:
  - `ALLOW_EXTRA_ROOTS`  
  - `SPEECH on/off`  
  - `MODEL_NAME`  
  - `CONFIRM_DANGEROUS true/false`

**Ejemplo:**  
> “Usa la carpeta de ayer” → Jarvis recuerda la última ruta usada.

---

#### 🧰 v4 — Acciones de PC comunes
**Objetivo:** asistente de productividad completo.

**Nuevas tools**
- `filesystem.delete` (archivos solo)  
- `filesystem.copy/move` (con seguridad y confirmación)  
- `apps.open` (VSCode, Chrome, Spotify …)  
- `browser.search_local` (opcional)

**Ejemplos**
- “Mueve `nota.txt` a Documentos”  
- “Abre VSCode en este proyecto”

---

#### 🏠 v5 — Domótica y automatización (opcional)
**Objetivo:** conectar Jarvis con el entorno físico.

**Ideas**
- Integración Home Assistant (API local)  
- Control de luces y enchufes locales  
- Mensajería (Discord/Telegram) para alertas  
- Programación de tareas locales (Task Scheduler)

---

### 🧱 Arquitectura general

- **Planner** (Razón + Acción): decide qué tool usar y valida entradas.  
- **Tools:** acciones atómicas (lectura, escritura, shell, voz, etc.).  
- **Policies:** rutas seguras y confirmaciones de comandos.  

---

### 🧾 Criterios de éxito

| Criterio | Descripción |
|-----------|-------------|
| **Seguridad** | Acciones fuera de `SAFE_ROOTS` → bloqueadas |
| **Determinismo** | Cada orden produce 1 acción única |
| **Trazas claras** | `TRACE (debug)` con tool-calls y resultados |
| **UX** | Mensajes claros en español, rutas Windows correctas |
| **Portabilidad** | Tests sin usar tu Escritorio real (`tmp_path`) |

---

### ⚠️ Riesgos y mitigación

- **LLM devuelve rutas POSIX** → normalización (hecha)  
- **Duplicados de acción** → “stop tras write” (hecho)  
- **Entornos corporativos (UNC)** → `ALLOW_EXTRA_ROOTS`  
- **Ollama caído** → modo fallback sin planificador  

---

### 📊 Estimaciones por fase

| Versión | Tiempo estimado | Resultado |
|----------|----------------|------------|
| v1 | 6–10 h | Jarvis Core funcional |
| v2 | 4–8 h | Voz (STT/TTS) |
| v3 | 4–8 h | Memoria y configuración |
| v4 | 6–10 h | Productividad y control de apps |
| v5 | >10 h | Integración doméstica real |

---

### 🧭 Filosofía de desarrollo

> “Cada feature nueva = una tool pequeña + una regla clara + una prueba.”  
>  
> No se rompe la seguridad ni el determinismo por añadir comodidad.  
> Jarvis crece como un asistente local inteligente, no como un riesgo sistémico.

---

**Última actualización:** 2025-10-22  
*(Roadmap base para desarrollo continuo de Jarvis local en Windows)*  


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