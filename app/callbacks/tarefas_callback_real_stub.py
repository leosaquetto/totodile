import json
import os

STATE_FILE = "data/tarefas/habitos_modelo.json"
FIELDS = ["cama", "louca", "banho", "dentes_manha"]


def load_state():
    if not os.path.exists(STATE_FILE):
        return {k: "❌" for k in FIELDS}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for key in FIELDS:
        data.setdefault(key, "❌")
    return data


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def toggle_from_callback_data(data, state):
    key = str(data).replace("tarefa_", "", 1)
    if key in FIELDS:
        state[key] = "✅" if state.get(key) == "❌" else "❌"
    return state
