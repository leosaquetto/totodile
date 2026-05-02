from app.callbacks.router_stub import dispatch


def handle_update(update):
    callback = update.get("callback_query")
    if callback:
        return dispatch(callback)
    return {"ok": False, "reason": "no_callback_query"}
