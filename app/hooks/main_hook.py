from app.config import ALLOWED_CHATS
from app.callbacks.router import dispatch
from app.commands.router import dispatch_command


def _message_from_update(update):
    for key in ("message", "edited_message"):
        value = update.get(key)
        if isinstance(value, dict):
            return key, value
    return None, {}


def _extract_chat_id(update):
    if not isinstance(update, dict):
        return None

    for key in ("message", "edited_message"):
        msg = update.get(key)
        if not isinstance(msg, dict):
            continue
        chat = msg.get("chat")
        if isinstance(chat, dict) and chat.get("id"):
            return chat["id"]

    callback = update.get("callback_query")
    if isinstance(callback, dict):
        msg = callback.get("message")
        if isinstance(msg, dict):
            chat = msg.get("chat")
            if isinstance(chat, dict) and chat.get("id"):
                return chat["id"]

    return None


def _is_allowed(update):
    if not ALLOWED_CHATS:
        return True
    chat_id = _extract_chat_id(update)
    return chat_id is not None and chat_id in ALLOWED_CHATS


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

    if not _is_allowed(update):
        return {"ok": False, "reason": "unauthorized_chat"}

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
