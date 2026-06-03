import json
import os
from datetime import date

from app.telegram_api import edit_message
from app.telegram_api_callbacks import answer_callback_query
from app.config import GROUP_ID

STATE_FILE = "data/academia/treino_state.json"
TREINOS = ["treino a", "treino b", "treino c"]


def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "proximo_treino": "treino a",
            "streak": 0,
            "ultimo_treino": "-"
        }
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("proximo_treino", "treino a")
    data.setdefault("streak", 0)
    data.setdefault("ultimo_treino", "-")
    return data


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def next_treino(current):
    normalized = str(current).strip().lower()
    if normalized not in TREINOS:
        return TREINOS[0]
    idx = TREINOS.index(normalized)
    return TREINOS[(idx + 1) % len(TREINOS)]


def build_text(state):
    return (
        f"🏋️ academia atualizado\n\n"
        f"próximo treino: {state.get('proximo_treino', '-')}\n"
        f"streak: {state.get('streak', 0)} dias\n"
        f"último treino: {state.get('ultimo_treino', '-')}"
    )


def handle(callback):
    if not isinstance(callback, dict):
        return {"ok": False, "reason": "invalid_callback"}

    data = str(callback.get("data") or "")
    msg = callback.get("message") if isinstance(callback.get("message"), dict) else {}
    callback_id = callback.get("id")

    state = load_state()
    hoje = date.today().isoformat()

    if data == "academia_done":
        state["ultimo_treino"] = hoje
        state["streak"] = int(state.get("streak", 0)) + 1
        state["proximo_treino"] = next_treino(state.get("proximo_treino", "treino a"))
        feedback = "treino registrado 💪"
    elif data == "academia_skip":
        state["ultimo_treino"] = hoje
        state["streak"] = 0
        state["proximo_treino"] = next_treino(state.get("proximo_treino", "treino a"))
        feedback = "treino pulado 🫠"
    else:
        feedback = "ação não reconhecida"

    save_state(state)
    message_id = msg.get("message_id")
    edit_result = None
    if message_id:
        edit_result = edit_message(GROUP_ID, message_id, build_text(state))
    answer_result = answer_callback_query(callback_id, feedback)

    return {
        "ok": True,
        "type": "academia_update",
        "edited": bool(edit_result),
        "answered": bool(answer_result and answer_result.get("ok")),
        "state": state
    }
