from pathlib import Path
from jarvis.tools import filesystem
from jarvis.permissions import SAFE_ROOTS

def test_filesystem_write_read_list_with_tmp_root(monkeypatch, tmp_path):
    # Simula que la raíz segura es la carpeta temporal del runner
    monkeypatch.setattr("jarvis.permissions.SAFE_ROOTS", [str(tmp_path)])

    # Escribe
    f = tmp_path / "hola_windows.txt"
    r = filesystem.write(path=str(f), text="Hola desde Windows")
    assert r.get("ok"), r

    # Lee
    rr = filesystem.read(path=str(f))
    assert rr.get("ok"), rr
    assert "Hola desde Windows" in rr.get("text", "")

    # Lista
    lst = filesystem.list(path=str(tmp_path))
    assert lst.get("ok"), lst
    items = [Path(p).name for p in lst.get("items", [])]
    assert "hola_windows.txt" in items
