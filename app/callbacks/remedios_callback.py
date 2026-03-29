import os
import json
from app.telegram_api import answer_callback_query, edit_message
from app.config import GROUP_ID

STATE_FILE = "data/remedios/prep_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def build_text(state):
    return (
        f"🐊 remédio atualizado\n\n"
        f"status: {state.get('status_hoje', 'pendente')}\n"
        f"estoque: {state.get('estoque_atual', 0)} cápsulas"
    )


def handle(callback):
    data = callback["data"]
    msg = callback["message"]

    state = load_state()

    if data == "prep_ok":
        state["status_hoje"] = "tomado ✅"
        state["estoque_atual"] = max(0, state.get("estoque_atual", 0) - 1)
    elif data == "prep_no":
        state["status_hoje"] = "não tomado ❌"
    elif data == "prep_later":
        state["status_hoje"] = "adiado ⏰"

    save_state(state)
    edit_message(GROUP_ID, msg["message_id"], build_text(state))
    answer_callback_query(callback["id"], "registrado 💚")
