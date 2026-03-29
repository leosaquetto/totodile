def handle(callback):
    return {
        "ok": True,
        "kind": "tarefa_stub",
        "data": callback.get("data")
    }
