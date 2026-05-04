import requests
from app.config import BOT_TOKEN

BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def _ensure_bot_token():
    if not BOT_TOKEN:
        raise RuntimeError("TOKEN_TOTODILE não configurado")


def send_message(chat_id, text, thread_id=None, reply_markup=None):
    _ensure_bot_token()
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if thread_id:
        payload["message_thread_id"] = thread_id

    if reply_markup:
        payload["reply_markup"] = reply_markup

    r = requests.post(f"{BASE}/sendMessage", json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(
            f"Telegram sendMessage failed: {r.status_code} {r.text} payload={payload}"
        )
    return r.json()


def edit_message(chat_id, message_id, text, reply_markup=None):
    _ensure_bot_token()
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    r = requests.post(f"{BASE}/editMessageText", json=payload, timeout=30)
    if not r.ok:
        raise RuntimeError(
            f"Telegram editMessageText failed: {r.status_code} {r.text} payload={payload}"
        )
    return r.json()
