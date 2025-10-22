from fastapi import FastAPI
from pydantic import BaseModel
from .planner import run_agent

app = FastAPI(title="Jarvis Local Agent (Qwen2.5-3B Q4)")

class AskBody(BaseModel):
    input: str
    max_steps: int = 5
    confirm: bool = True

@app.post("/ask")
def ask(body: AskBody):
    return run_agent(body.input, confirm=body.confirm, max_steps=body.max_steps)
