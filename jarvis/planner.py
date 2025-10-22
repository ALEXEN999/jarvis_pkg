# jarvis/planner.py
import json
from typing import Dict, Any, List
from pathlib import Path

from .llm import chat, SYSTEM_PREFIX
from .tools import TOOL_REGISTRY
from .permissions import SAFE_ROOTS, is_safe_path, needs_confirmation_for_shell


def _desktop_root() -> str | None:
    # elige la primera ruta de Escritorio detectada (si existe)
    for r in SAFE_ROOTS:
        p = Path(r)
        name = p.name.lower()
        if p.exists() and (name == "desktop" or name == "escritorio"):
            return str(p.resolve())
    return None


def _normalize_path(raw: str, user_input: str) -> str:
    """
    Convierte rutas POSIX o vagas a una ruta Windows segura:
    - Si el usuario dijo 'Escritorio'/'Desktop', fuerza a usar el Escritorio detectado.
    - Si viene con '/', convierte a backslashes.
    - Si no es segura, intenta reubicar al Escritorio (conservando el nombre del archivo).
    """
    if not raw:
        # Si no hay path pero el usuario menciona Escritorio/Desktop, usa el Escritorio
        ui = (user_input or "").lower()
        desktop = _desktop_root()
        if desktop and ("escritorio" in ui or "desktop" in ui):
            return desktop
        return raw

    path = raw.replace("/", "\\")  # POSIX -> Windows
    ui = (user_input or "").lower()
    desktop = _desktop_root()

    # Caso especial: el path ES literalmente "Escritorio" o "Desktop"
    simple = path.strip().strip("\\/").lower()
    if desktop and simple in ("escritorio", "desktop"):
        return desktop

    # Si el usuario menciona Escritorio/Desktop y el path es relativo: colócalo dentro del Escritorio
    try:
        p = Path(path)
        if desktop and ("escritorio" in ui or "desktop" in ui) and not p.is_absolute():
            # Si el relativo es solo un nombre (no una ruta con subdirs), úsalo dentro del Escritorio
            name = p.name or "output.txt"
            return str(Path(desktop) / name)
    except Exception:
        # Fallback robusto
        if desktop and ("escritorio" in ui or "desktop" in ui):
            return str(Path(desktop) / Path(path).name)

    # Si sigue sin ser segura, reubica al Escritorio conservando el basename
    if desktop and not is_safe_path(path):
        try:
            name = Path(path).name
        except Exception:
            name = "output.txt"
        return str(Path(desktop) / name)

    return path



def _system() -> Dict[str, str]:
    return {"role": "system", "content": SYSTEM_PREFIX}


def _is_tool_call(text: str) -> bool:
    t = text.strip()
    return t.startswith("{") and t.endswith("}")


def run_agent(user_input: str, confirm: bool = True, max_steps: int = 5) -> Dict[str, Any]:
    messages: List[Dict[str, str]] = [_system(), {"role": "user", "content": user_input}]
    trace: List[Dict[str, Any]] = []

    for _ in range(max_steps):
        reply = chat(messages)
        trace.append({"assistant": reply})

        # Si no es tool-call en JSON, respuesta final
        if not _is_tool_call(reply):
            return {"final": reply, "trace": trace}

        # Parseo seguro de la tool-call
        try:
            call = json.loads(reply)
            tool_name = call.get("tool", "")
            args = call.get("args") or {}
            # Normalización de rutas antes de ejecutar la tool
            if tool_name.startswith("filesystem."):
                if "path" in args and isinstance(args["path"], str):
                    args["path"] = _normalize_path(args["path"], user_input)
        except Exception as e:
            return {"final": f"Error parsing tool call: {e}\nRaw: {reply}", "trace": trace}

        # Seguridad + dispatch
        if tool_name.startswith("filesystem."):
            p = args.get("path") or args.get("dest") or ""
            if p and not is_safe_path(p):
                result = {"ok": False, "error": f"Path not allowed by policy: {p}"}
            else:
                func = TOOL_REGISTRY.get(tool_name)
                result = func(**args) if func else {"ok": False, "error": f"Unknown tool {tool_name}"}

        elif tool_name == "shell.run":
            cmd = args.get("command", "")
            if confirm and needs_confirmation_for_shell(cmd):
                result = {"ok": False, "error": f"Command requires confirmation: {cmd}"}
            else:
                func = TOOL_REGISTRY.get(tool_name)
                result = func(**args) if func else {"ok": False, "error": f"Unknown tool {tool_name}"}

        else:
            result = {"ok": False, "error": f"Unknown tool {tool_name}"}

        # Registrar TOOL_RESULT en el diálogo ReAct
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"TOOL_RESULT: {json.dumps(result)}"})
        
        # ✅ Respuesta determinista para listados (evita que el LLM "se invente" cosas)
        if tool_name == "filesystem.list":
            if result.get("ok"):
                items = result.get("items") or []
                # Formatear nombres (basename), ignorar rutas completas
                pretty = [Path(p).name for p in items]
                if not pretty:
                    return {
                        "final": "Tu Escritorio está vacío." if "escritorio" in user_input.lower() else "La carpeta está vacía.",
                        "trace": trace
                    }
                # Mensaje amigable
                title = "Aquí están los archivos en tu Escritorio:" if "escritorio" in user_input.lower() else "Contenido de la carpeta:"
                lines = "\n".join(f"{i}. {name}" for i, name in enumerate(pretty, start=1))
                return {"final": f"{title}\n\n{lines}", "trace": trace}
            else:
                return {"final": f"No pude listar: {result.get('error')}", "trace": trace}

        # 🔒 Stop tras primer write exitoso (para evitar duplicados)
        if tool_name == "filesystem.write" and result.get("ok"):
            filename = Path(args.get("path", "")).name or "el archivo"
            return {"final": f"El archivo '{filename}' ha sido creado correctamente.", "trace": trace}

    return {"final": "He alcanzado el máximo de pasos. ¿Quieres que continúe?", "trace": trace}
