import requests
from app.config import BOT_TOKEN

BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, thread_id=None, reply_markup=None):
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
    r.raise_for_status()
    return r.json()

def edit_message(chat_id, message_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    r = requests.post(f"{BASE}/editMessageText", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
