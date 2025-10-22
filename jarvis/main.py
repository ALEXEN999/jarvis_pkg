import argparse, json
from .planner import run_agent

def main():
    parser = argparse.ArgumentParser(
        description="Jarvis local agent (Qwen2.5-3B Q4 via Ollama)"
    )
    parser.add_argument("q", type=str, help="Instrucción en lenguaje natural entre comillas")
    parser.add_argument("--no-confirm", action="store_true",
                        help="No pedir confirmación para comandos de shell peligrosos")
    parser.add_argument("--max-steps", type=int, default=5,
                        help="Máximo de pasos ReAct (por defecto: 5)")
    args = parser.parse_args()

    result = run_agent(args.q, confirm=not args.no_confirm, max_steps=args.max_steps)
    print("\n=== JARVIS RESPONSE ===\n")
    print(result.get("final", ""))
    print("\n--- TRACE (debug) ---")
    print(json.dumps(result.get("trace", []), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
