import os
import json
from pathlib import Path

from app.modules import remedios, tarefas_domesticas, academia

BASE_DIR = Path(__file__).resolve().parent.parent


def load_json(relative_path, fallback):
    path = BASE_DIR / relative_path
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def run():
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

    remedios.send_prep(prep_state)
    tarefas_domesticas.send_panel(tarefas_state)
    academia.send_academia(academia_state)


if __name__ == "__main__":
    run()
