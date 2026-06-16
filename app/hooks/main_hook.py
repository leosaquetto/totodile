from app.callbacks.router import dispatch
from app.commands.router import dispatch_command


def _message_from_update(update):
    for key in ("message", "edited_message"):
        value = update.get(key)
        if isinstance(value, dict):
            return key, value
    return None, {}


def _chat_context(message):
    if not isinstance(message, dict):
        return None
    chat = message.get("chat") if isinstance(message.get("chat"), dict) else None
    if not chat:
        return None
    return {
        "chat_id": chat.get("id"),
        "message_thread_id": message.get("message_thread_id"),
    }


def handle_update(update):
    if not isinstance(update, dict):
        return {"ok": False, "reason": "invalid_update"}

    callback = update.get("callback_query")
    if isinstance(callback, dict):
        return dispatch(callback)
    if callback is not None:
        return {"ok": False, "reason": "invalid_callback_query"}

    message_type, message = _message_from_update(update)
    text = message.get("text")
    if isinstance(text, str) and text.strip():
        result = dispatch_command(text, message=message)
        result.setdefault("message_type", message_type)
        return result

    return {"ok": False, "reason": "no_callback_or_text"}
