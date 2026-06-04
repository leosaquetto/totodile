from app.callbacks.tarefas_state import load_state, save_state, toggle_from_callback_data
from app.config import GROUP_ID
from app.modules import tarefas_domesticas
from app.telegram_api import edit_message
from app.telegram_api_callbacks import answer_callback_query


def handle(callback):
    if not isinstance(callback, dict):
        return {"ok": False, "reason": "invalid_callback"}

    data = str(callback.get("data") or "")
    msg = callback.get("message") if isinstance(callback.get("message"), dict) else {}
    callback_id = callback.get("id")

    state = load_state()
    changed, state = toggle_from_callback_data(data, state)
    if not changed:
        answer_result = answer_callback_query(callback_id, "ação não reconhecida")
        return {
            "ok": False,
            "reason": "unknown_task",
            "answered": bool(answer_result and answer_result.get("ok")),
        }

    answer_result = answer_callback_query(callback_id, "tarefa atualizada")
    save_state(state)

    edit_result = None
    message_id = msg.get("message_id")
    chat = msg.get("chat") if isinstance(msg.get("chat"), dict) else {}
    chat_id = chat.get("id") or GROUP_ID
    if message_id and chat_id:
        edit_result = edit_message(
            chat_id,
            message_id,
            tarefas_domesticas.render_text(state),
            reply_markup=tarefas_domesticas.build_keyboard(state),
        )

    return {
        "ok": True,
        "type": "tarefas_update",
        "edited": bool(edit_result),
        "answered": bool(answer_result and answer_result.get("ok")),
        "state": state
    }
