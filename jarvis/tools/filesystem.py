from typing import Dict, Any
from pathlib import Path

def read(path: str) -> Dict[str, Any]:
    try:
        p = Path(path)
        if not p.exists():
            return {"ok": False, "error": "File not found."}
        return {"ok": True, "content": p.read_text(encoding="utf-8", errors="ignore")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def write(path: str, text: str) -> Dict[str, Any]:
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def list(path: str) -> Dict[str, Any]:
    try:
        p = Path(path)
        if not p.exists():
            return {"ok": False, "error": "Path not found."}
        items = [str(x) for x in p.iterdir()]
        return {"ok": True, "items": items}
    except Exception as e:
        return {"ok": False, "error": str(e)}
