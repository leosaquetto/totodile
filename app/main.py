import os
import json
from pathlib import Path

from app.modules import remedios, tarefas_domesticas, academia, lembretes
from app.config import BOT_TOKEN, GROUP_ID

BASE_DIR = Path(__file__).resolve().parent.parent


def validate_runtime_config():
    return {
        "has_token": bool(BOT_TOKEN),
        "has_group_id": bool(GROUP_ID),
    }



def load_json(relative_path, fallback):
    path = BASE_DIR / relative_path
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def run():
    cfg = validate_runtime_config()
    print(f"[totodile] config has_token={cfg['has_token']} has_group_id={cfg['has_group_id']}")
    prep_state = load_json("data/remedios/prep_state.json", {
        "status_hoje": "pendente",
        "estoque_atual": 64
    })

    tarefas_state = load_json("data/tarefas/habitos_modelo.json", {
        "cama": "❌",
        "louca": "❌",
        "banho": "✅",
        "dentes_manha": "✅"
    })

    academia_state = load_json("data/academia/treino_state.json", {
        "proximo_treino": "treino a",
        "streak": 4,
        "ultimo_treino": "ontem"
    })

    lembretes.send_due_reminders()
    # Pausa temporária dos envios de rotina solicitados (academia, tarefas e saúde/remédios).
    # Mantém os demais envios funcionando normalmente.
    # remedios.send_prep(prep_state)
    # tarefas_domesticas.send_panel(tarefas_state)
    # academia.send_academia(academia_state)


if __name__ == "__main__":
    run()
