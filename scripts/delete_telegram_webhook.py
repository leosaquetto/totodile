#!/usr/bin/env python3

import argparse
import json
import os
import sys

import requests

TELEGRAM_API_BASE = "https://api.telegram.org"


def _required_env(name):
    value = os.getenv(name)
    if not value:
        print(f"erro: env {name} não configurada", file=sys.stderr)
        sys.exit(2)
    return value


def _print_json(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description="Remove o webhook do Telegram.")
    parser.add_argument(
        "--drop-pending-updates",
        action="store_true",
        help="descarta updates pendentes ao remover o webhook",
    )
    args = parser.parse_args()

    token = _required_env("TOKEN_TOTODILE")
    payload = {"drop_pending_updates": bool(args.drop_pending_updates)}

    try:
        response = requests.post(
            f"{TELEGRAM_API_BASE}/bot{token}/deleteWebhook",
            json=payload,
            timeout=30,
        )
        response_json = response.json()
    except requests.RequestException as exc:
        print(f"erro: falha ao chamar Telegram deleteWebhook ({exc.__class__.__name__})", file=sys.stderr)
        return 1
    except ValueError:
        print("erro: Telegram retornou resposta não JSON", file=sys.stderr)
        print(response.text)
        return 1

    _print_json(response_json)
    return 0 if isinstance(response_json, dict) and response_json.get("ok") is True else 1


if __name__ == "__main__":
    sys.exit(main())
