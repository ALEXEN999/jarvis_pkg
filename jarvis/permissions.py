from pathlib import Path
import os
import sys

def _candidate_desktops() -> list[str]:
    """
    Devuelve posibles rutas de Escritorio en Windows (inglés/español y OneDrive),
    más equivalentes multiplataforma por si se usa en WSL u otros entornos.
    Solo se incluirán las que existan realmente en el sistema.
    """
    cands: list[Path] = []

    # USERPROFILE típico de Windows: C:\Users\alexp
    user = os.environ.get("USERPROFILE")
    if user:
        up = Path(user)
        cands += [up / "Desktop", up / "Escritorio"]

    # OneDrive (si el Escritorio está redirigido allí)
    od = os.environ.get("OneDrive")
    if od:
        odp = Path(od)
        cands += [odp / "Desktop", odp / "Escritorio"]

    # Fallback genérico por si se ejecuta en otro entorno
    home = Path.home()
    cands += [home / "Desktop", home / "Escritorio"]

    # Filtrar solo las rutas existentes
    uniq: list[str] = []
    seen = set()
    for p in cands:
        try:
            rp = str(p.resolve())
        except Exception:
            rp = str(p)
        if os.path.isdir(rp) and rp.lower() not in seen:
            seen.add(rp.lower())
            uniq.append(rp)
    return uniq

# Rutas seguras calculadas dinámicamente:
SAFE_ROOTS = _candidate_desktops() + [str(Path.cwd())]

# Comandos de shell que requieren confirmación explícita
DANGEROUS_CMDS = ["del ", " rm ", "rmdir", "format", "shutdown", "reboot", "sc stop", "reg delete"]

def _normcase(path: str) -> str:
    # Comparación case-insensitive en Windows
    return path.lower() if sys.platform.startswith("win") else path

def is_safe_path(path: str) -> bool:
    """
    Permite acceso solo si la ruta objetivo está dentro de alguna SAFE_ROOT.
    """
    try:
        target = _normcase(str(Path(path).resolve()))
        for root in SAFE_ROOTS:
            try:
                base = _normcase(str(Path(root).resolve()))
            except Exception:
                base = _normcase(root)
            if target.startswith(base):
                return True
        return False
    except Exception:
        return False

def needs_confirmation_for_shell(command: str) -> bool:
    c = command.lower().strip()
    return any(k in c for k in DANGEROUS_CMDS)
