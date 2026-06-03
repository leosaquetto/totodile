import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.hooks.main_hook import handle_update


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print("erro: nenhum JSON recebido via stdin", file=sys.stderr)
        sys.exit(1)

    try:
        update = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"erro: JSON inválido ({exc.msg} na linha {exc.lineno}, coluna {exc.colno})", file=sys.stderr)
        sys.exit(1)

    result = handle_update(update)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
