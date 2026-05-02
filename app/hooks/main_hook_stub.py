from app.callbacks.router_stub import dispatch
from app.commands.router import dispatch_command



def handle_update(update):
    callback = update.get("callback_query")
    if callback:
        return dispatch(callback)

    message = update.get("message") or {}
    text = message.get("text")
    if text:
        return dispatch_command(text)

    return {"ok": False, "reason": "no_callback_or_text"}
