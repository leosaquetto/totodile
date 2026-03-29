from app.callbacks import remedios_callback
from app.callbacks import tarefas_callback_stub


def dispatch(callback):
    data = callback.get("data", "")

    if data.startswith("prep_"):
        return remedios_callback.handle(callback)

    if data.startswith("tarefa_"):
        return tarefas_callback_stub.handle(callback)

    return {"ok": False, "reason": "unhandled_callback", "data": data}
