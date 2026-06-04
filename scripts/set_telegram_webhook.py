#!/usr/bin/env python3

import json
import os
import sys

import requests

TELEGRAM_API_BASE = "https://api.telegram.org"
ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]


def _required_env(name):
    value = os.getenv(name)
    if not value:
        print(f"erro: env {name} não configurada", file=sys.stderr)
        sys.exit(2)
    return value


def _print_json(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main():
    token = _required_env("TOKEN_TOTODILE")
    webhook_url = _required_env("TELEGRAM_WEBHOOK_URL")
    secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")

    payload = {
        "url": webhook_url,
        "allowed_updates": ALLOWED_UPDATES,
        "drop_pending_updates": False,
    }
    if secret:
        payload["secret_token"] = secret

    try:
        response = requests.post(
            f"{TELEGRAM_API_BASE}/bot{token}/setWebhook",
            json=payload,
            timeout=30,
        )
        response_json = response.json()
    except requests.RequestException as exc:
        print(f"erro: falha ao chamar Telegram setWebhook ({exc.__class__.__name__})", file=sys.stderr)
        return 1
    except ValueError:
        print("erro: Telegram retornou resposta não JSON", file=sys.stderr)
        print(response.text)
        return 1

    _print_json(response_json)
    return 0 if isinstance(response_json, dict) and response_json.get("ok") is True else 1


if __name__ == "__main__":
    sys.exit(main())
