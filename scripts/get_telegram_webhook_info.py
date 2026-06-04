#!/usr/bin/env python3

import json
import os
import sys

import requests

TELEGRAM_API_BASE = "https://api.telegram.org"
SUMMARY_FIELDS = [
    "url",
    "pending_update_count",
    "last_error_date",
    "last_error_message",
    "allowed_updates",
]


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

    try:
        response = requests.get(f"{TELEGRAM_API_BASE}/bot{token}/getWebhookInfo", timeout=30)
        response_json = response.json()
    except requests.RequestException as exc:
        print(f"erro: falha ao chamar Telegram getWebhookInfo ({exc.__class__.__name__})", file=sys.stderr)
        return 1
    except ValueError:
        print("erro: Telegram retornou resposta não JSON", file=sys.stderr)
        print(response.text)
        return 1

    result = response_json.get("result") if isinstance(response_json, dict) else None
    if isinstance(result, dict):
        summary = {field: result.get(field) for field in SUMMARY_FIELDS}
        print("Resumo:")
        _print_json(summary)
        print("\nResposta completa:")

    _print_json(response_json)
    return 0 if isinstance(response_json, dict) and response_json.get("ok") is True else 1


if __name__ == "__main__":
    sys.exit(main())
