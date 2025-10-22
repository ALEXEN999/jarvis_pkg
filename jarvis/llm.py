"""
Lightweight wrapper around a local LLM backend.

This module attempts to communicate with a local Ollama server via HTTPX. To
gracefully handle environments where the `httpx` package is unavailable or
the backend cannot be reached, it falls back to returning an informative
error message instead of raising an exception. The agent is designed to
operate without network access by using a stub response when necessary.
"""

from typing import List, Dict

# Try importing httpx. If unavailable, set a flag and use a stub fallback
try:
    import httpx  # type: ignore
    _HAS_HTTPX = True
except Exception:
    httpx = None  # type: ignore
    _HAS_HTTPX = False


OLLAMA_HOST = "http://localhost:11434"
MODEL = "qwen2.5:3b-instruct-q4_0"  # único modelo por defecto

# System prompt instructing the LLM how to behave
SYSTEM_PREFIX = """You are Jarvis, a helpful local PC agent.

ENVIRONMENT:
- The user is on Windows (Spanish locale). The desktop folder is "Escritorio" or "Desktop".
- Always use Windows absolute paths (e.g., C:\\Users\\alexp\\Escritorio\\file.txt). Never /home/...

TOOLS:
- filesystem.read(path)
- filesystem.write(path, text)
- filesystem.list(path)
- shell.run(command)

RULES:
- If a tool is needed, reply with ONE SINGLE JSON object: {"tool": "<name>", "args": {...}}.
- Make AT MOST ONE tool call per user request unless the TOOL_RESULT explicitly asks you to retry.
- NEVER perform the same write twice or write to a different filename than the user asked unless the user explicitly requests it.
- Otherwise, reply in natural language (no JSON).
- Keep steps minimal.
- When the user says "Escritorio", use the actual Windows Desktop path.
"""




def chat(messages: List[Dict[str, str]]) -> str:
    """Send a chat request to the local LLM or return a stub reply.

    Args:
        messages: A list of message dicts in the format {"role": str, "content": str}.

    Returns:
        The content of the assistant's reply. If the backend is unavailable or
        httpx is not installed, returns an explanatory error message.
    """
    # If httpx is not available, return a placeholder response
    if not _HAS_HTTPX:
        return "Lo siento, el modelo LLM no está disponible en este entorno."
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {"model": MODEL, "messages": messages, "stream": False}
    try:
        with httpx.Client(timeout=120) as client:  # type: ignore
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            return data.get("message", {}).get("content", "")
    except Exception as e:
        # Fallback stub response when the backend is unreachable
        return f"Lo siento, no pude comunicarme con el modelo LLM: {e}"
