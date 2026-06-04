import json

import requests

from app.config import BOT_TOKEN

TELEGRAM_API_BASE = "https://api.telegram.org"


def _truncate(value, limit=1200):
    text = str(value)
    if len(text) <= limit:
        return text
    return f"{text[:limit]}...<truncated>"


def _safe_payload(payload):
    if not isinstance(payload, dict):
        return payload
    return {key: value for key, value in payload.items() if key not in {"token"}}


def _ensure_bot_token():
    if not BOT_TOKEN:
        raise RuntimeError("TOKEN_TOTODILE não configurado")


def _telegram_url(method):
    _ensure_bot_token()
    return f"{TELEGRAM_API_BASE}/bot{BOT_TOKEN}/{method}"


def _json_reply_markup(reply_markup):
    if reply_markup is None:
        return None
    if isinstance(reply_markup, str):
        return reply_markup
    return json.dumps(reply_markup, ensure_ascii=False)


def _post(method, payload):
    try:
        response = requests.post(_telegram_url(method), json=payload, timeout=30)
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Telegram {method} request failed: {exc.__class__.__name__} "
            f"payload={_safe_payload(payload)}"
        ) from None

    try:
        response_json = response.json()
    except ValueError:
        response_json = None

    if not response.ok:
        response_body = response_json if response_json is not None else response.text
        raise RuntimeError(
            f"Telegram {method} failed: status={response.status_code} "
            f"response={_truncate(response_body)} payload={_safe_payload(payload)}"
        )

    if response_json is None:
        raise RuntimeError(
            f"Telegram {method} returned non-JSON response: "
            f"status={response.status_code} response={_truncate(response.text)} "
            f"payload={_safe_payload(payload)}"
        )

    if not isinstance(response_json, dict) or response_json.get("ok") is not True:
        raise RuntimeError(
            f"Telegram {method} returned API error: status={response.status_code} "
            f"response={_truncate(response_json)} payload={_safe_payload(payload)}"
        )

    return response_json


def send_message(chat_id, text, thread_id=None, reply_markup=None, parse_mode=None):
    if not chat_id:
        raise RuntimeError("chat_id não configurado")

    payload = {
        "chat_id": chat_id,
        "text": "" if text is None else str(text),
    }

    if parse_mode:
        payload["parse_mode"] = parse_mode

    if thread_id:
        payload["message_thread_id"] = thread_id

    if reply_markup:
        payload["reply_markup"] = _json_reply_markup(reply_markup)

    return _post("sendMessage", payload)


def edit_message(chat_id, message_id, text, reply_markup=None, parse_mode=None):
    if not chat_id:
        raise RuntimeError("chat_id não configurado")
    if not message_id:
        raise RuntimeError("message_id não configurado")

    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": "" if text is None else str(text),
    }

    if parse_mode:
        payload["parse_mode"] = parse_mode

    if reply_markup:
        payload["reply_markup"] = _json_reply_markup(reply_markup)

    return _post("editMessageText", payload)


def answer_callback_query(callback_query_id, text=None, show_alert=None, cache_time=None):
    if not callback_query_id:
        return {"ok": False, "reason": "missing_callback_query_id"}

    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = str(text)
    if show_alert is not None:
        payload["show_alert"] = bool(show_alert)
    if cache_time is not None:
        payload["cache_time"] = int(cache_time)

    return _post("answerCallbackQuery", payload)
