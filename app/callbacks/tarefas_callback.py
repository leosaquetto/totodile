from app.callbacks.tarefas_callback_real_stub import load_state, save_state, toggle_from_callback_data


def handle(callback):
    data = callback.get("data", "")

    state = load_state()
    state = toggle_from_callback_data(data, state)
    save_state(state)

    return {
        "ok": True,
        "type": "tarefas_update",
        "state": state
    }
