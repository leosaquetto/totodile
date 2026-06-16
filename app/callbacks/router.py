from app.callbacks import remedios_callback
from app.callbacks import tarefas_callback
from app.callbacks import academia_callback
from app.callbacks import agenda_callback
from app.telegram_api_callbacks import answer_callback_query


def _answer_unhandled(callback, text):
    callback_id = callback.get("id") if isinstance(callback, dict) else None
    if not callback_id:
        return None
    return answer_callback_query(callback_id, text)


def dispatch(callback):
    if not isinstance(callback, dict):
        return {"ok": False, "reason": "invalid_callback"}

    data = str(callback.get("data") or "")

    if data.startswith("prep_"):
        return remedios_callback.handle(callback)

    if data.startswith("tarefa_"):
        return tarefas_callback.handle(callback)

    if data.startswith("academia_"):
        return academia_callback.handle(callback)

    if data.startswith("agenda_") or data.startswith("aniversarios_") or data.startswith("rotina_") or data.startswith("menu_"):
        return agenda_callback.handle(callback)

    _answer_unhandled(callback, "ação não reconhecida")
    return {"ok": False, "reason": "unhandled_callback", "data": data}
