from app.storage import load_json, save_json

STATE_FILE = "data/tarefas/habitos_modelo.json"
FIELDS = ["cama", "louca", "banho", "dentes_manha"]
DEFAULT_STATE = {key: "❌" for key in FIELDS}


def load_state():
    data = load_json(STATE_FILE, DEFAULT_STATE)
    if not isinstance(data, dict):
        data = dict(DEFAULT_STATE)
    for key in FIELDS:
        data.setdefault(key, "❌")
    return data


def save_state(state):
    return save_json(STATE_FILE, state, "🤖 atualizar tarefas")


def toggle_from_callback_data(data, state):
    key = str(data).replace("tarefa_", "", 1)
    if key in FIELDS:
        state[key] = "✅" if state.get(key) == "❌" else "❌"
        return True, state
    return False, state
