"""
Cross‑platform shell execution utility for Jarvis.

This module attempts to run commands using the most appropriate shell available
on the host system. On Windows it prefers PowerShell (pwsh or powershell),
while on POSIX systems it falls back to bash or sh. It returns a dictionary
with the execution status, captured stdout/stderr, and return code.
"""

from shutil import which
import subprocess
from typing import Dict, Any


def _pick_shell() -> str:
    """Return the name of an available shell executable.

    Priority order:
        1. pwsh (PowerShell 7+)
        2. powershell (Windows PowerShell)
        3. bash
        4. sh

    Returns:
        The first available shell name.

    Raises:
        FileNotFoundError: If no suitable shell is found.
    """
    for candidate in ("pwsh", "powershell", "bash", "sh"):
        if which(candidate):
            return candidate
    raise FileNotFoundError("No suitable shell found on the system")


def run(command: str) -> Dict[str, Any]:
    """Run a shell command and return execution details.

    Args:
        command: The command to execute as a string.

    Returns:
        A dictionary containing:
            - ok (bool): Whether execution was attempted successfully.
            - stdout (str): Captured standard output (on success).
            - stderr (str): Captured standard error (on success).
            - code (int): Return code of the process (on success).
            - error (str): Error message if the command could not be executed.
    """
    try:
        exe = _pick_shell()
        # Construct command arguments depending on shell type
        if exe in ("pwsh", "powershell"):
            args = [exe, "-NoLogo", "-NoProfile", "-Command", command]
        else:
            # POSIX shells (bash/sh) use -c to execute the command string
            args = [exe, "-c", command]
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return {
            "ok": True,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "code": completed.returncode,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
