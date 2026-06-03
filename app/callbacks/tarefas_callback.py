from app.callbacks.tarefas_callback_real_stub import load_state, save_state, toggle_from_callback_data
from app.telegram_api_callbacks import answer_callback_query


def handle(callback):
    if not isinstance(callback, dict):
        return {"ok": False, "reason": "invalid_callback"}

    data = str(callback.get("data") or "")

    state = load_state()
    state = toggle_from_callback_data(data, state)
    save_state(state)
    answer_result = answer_callback_query(callback.get("id"), "tarefa atualizada")

    return {
        "ok": True,
        "type": "tarefas_update",
        "answered": bool(answer_result and answer_result.get("ok")),
        "state": state
    }
