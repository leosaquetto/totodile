import json
import os
from datetime import date

STATE_FILE = "data/academia/treino_state.json"
TREINOS = ["treino a", "treino b", "treino c"]


def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "proximo_treino": "treino a",
            "streak": 0,
            "ultimo_treino": ""
        }
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("proximo_treino", "treino a")
    data.setdefault("streak", 0)
    data.setdefault("ultimo_treino", "")
    return data


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def apply_from_callback_data(data, state):
    action = str(data).replace("academia_", "", 1)
    today = str(date.today())

    if action == "feito":
        current = state.get("proximo_treino", "treino a")
        idx = TREINOS.index(current) if current in TREINOS else 0
        state["proximo_treino"] = TREINOS[(idx + 1) % len(TREINOS)]
        state["streak"] = state.get("streak", 0) + 1
        state["ultimo_treino"] = today

    elif action == "pular":
        current = state.get("proximo_treino", "treino a")
        idx = TREINOS.index(current) if current in TREINOS else 0
        state["proximo_treino"] = TREINOS[(idx + 1) % len(TREINOS)]
        state["streak"] = 0
        state["ultimo_treino"] = today

    return state


def handle(callback):
    data = callback.get("data", "")

    state = load_state()
    state = apply_from_callback_data(data, state)
    save_state(state)

    return {
        "ok": True,
        "type": "academia_update",
        "state": state
    }
