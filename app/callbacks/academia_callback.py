from datetime import date

from app.telegram_api import edit_message
from app.telegram_api_callbacks import answer_callback_query
from app.config import GROUP_ID
from app.storage import load_json, save_json
from app.modules import academia

STATE_FILE = "data/academia/treino_state.json"
TREINOS = ["treino a", "treino b", "treino c"]
DEFAULT_STATE = {
    "proximo_treino": "treino a",
    "streak": 0,
    "ultimo_treino": "-",
}


def load_state():
    data = load_json(STATE_FILE, DEFAULT_STATE)
    if not isinstance(data, dict):
        data = dict(DEFAULT_STATE)
    data.setdefault("proximo_treino", "treino a")
    data.setdefault("streak", 0)
    data.setdefault("ultimo_treino", "-")
    return data


def save_state(state):
    return save_json(STATE_FILE, state, "🤖 atualizar academia")


def next_treino(current):
    normalized = str(current).strip().lower()
    if normalized not in TREINOS:
        return TREINOS[0]
    idx = TREINOS.index(normalized)
    return TREINOS[(idx + 1) % len(TREINOS)]


def _int_value(value, fallback=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


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
        state["streak"] = _int_value(state.get("streak")) + 1
        state["proximo_treino"] = next_treino(state.get("proximo_treino", "treino a"))
        feedback = "treino registrado 💪"
    elif data == "academia_skip":
        state["ultimo_treino"] = hoje
        state["streak"] = 0
        state["proximo_treino"] = next_treino(state.get("proximo_treino", "treino a"))
        feedback = "treino pulado 🫠"
    else:
        feedback = "ação não reconhecida"
        answer_result = answer_callback_query(callback_id, feedback)
        return {
            "ok": False,
            "reason": "unknown_academia_action",
            "answered": bool(answer_result and answer_result.get("ok")),
        }

    answer_result = answer_callback_query(callback_id, feedback)
    save_state(state)
    message_id = msg.get("message_id")
    edit_result = None
    chat = msg.get("chat") if isinstance(msg.get("chat"), dict) else {}
    chat_id = chat.get("id") or GROUP_ID
    if message_id and chat_id:
        edit_result = edit_message(
            chat_id,
            message_id,
            build_text(state),
            reply_markup=academia.build_keyboard(),
        )

    return {
        "ok": True,
        "type": "academia_update",
        "edited": bool(edit_result),
        "answered": bool(answer_result and answer_result.get("ok")),
        "state": state
    }
