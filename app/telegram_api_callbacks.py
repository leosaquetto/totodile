from app.telegram_api import BASE
import requests


def answer_callback_query(callback_query_id, text=None):
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
    r = requests.post(f"{BASE}/answerCallbackQuery", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
