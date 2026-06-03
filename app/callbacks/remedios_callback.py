from app.telegram_api import edit_message
from app.telegram_api_callbacks import answer_callback_query
from app.config import GROUP_ID
from app.storage import load_json, save_json
from app.modules import remedios

STATE_FILE = "data/remedios/prep_state.json"
DEFAULT_STATE = {
    "status_hoje": "pendente",
    "estoque_atual": 0,
}


def load_state():
    state = load_json(STATE_FILE, DEFAULT_STATE)
    if not isinstance(state, dict):
        state = dict(DEFAULT_STATE)
    state.setdefault("status_hoje", "pendente")
    state.setdefault("estoque_atual", 0)
    return state


def save_state(state):
    return save_json(STATE_FILE, state, "🤖 atualizar remédios")


def build_text(state):
    return (
        f"🐊 remédio atualizado\n\n"
        f"status: {state.get('status_hoje', 'pendente')}\n"
        f"estoque: {state.get('estoque_atual', 0)} cápsulas"
    )


def _int_value(value, fallback=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def handle(callback):
    if not isinstance(callback, dict):
        return {"ok": False, "reason": "invalid_callback"}

    data = str(callback.get("data") or "")
    msg = callback.get("message") if isinstance(callback.get("message"), dict) else {}
    callback_id = callback.get("id")

    state = load_state()

    if data == "prep_ok":
        state["status_hoje"] = "tomado ✅"
        state["estoque_atual"] = max(0, _int_value(state.get("estoque_atual")) - 1)
    elif data == "prep_no":
        state["status_hoje"] = "não tomado ❌"
    elif data == "prep_later":
        state["status_hoje"] = "adiado ⏰"
    else:
        answer_result = answer_callback_query(callback_id, "ação não reconhecida")
        return {
            "ok": False,
            "reason": "unknown_remedio_action",
            "answered": bool(answer_result and answer_result.get("ok")),
        }

    answer_result = answer_callback_query(callback_id, "registrado 💚")
    save_state(state)
    message_id = msg.get("message_id")
    edit_result = None
    chat = msg.get("chat") if isinstance(msg.get("chat"), dict) else {}
    chat_id = chat.get("id") or GROUP_ID
    if message_id:
        edit_result = edit_message(chat_id, message_id, build_text(state), reply_markup=remedios.build_keyboard())

    return {
        "ok": True,
        "type": "remedios_update",
        "edited": bool(edit_result),
        "answered": bool(answer_result and answer_result.get("ok")),
        "state": state
    }
