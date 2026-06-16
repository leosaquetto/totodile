#!/usr/bin/env python3

import json
import os
import sys

import requests

TELEGRAM_API_BASE = "https://api.telegram.org"
COMMANDS = [
    {"command": "menu", "description": "abrir menu principal"},
    {"command": "start", "description": "abrir menu principal"},
    {"command": "agenda", "description": "ver agenda de hoje"},
    {"command": "agenda_hoje", "description": "ver eventos de hoje"},
    {"command": "agenda_semana", "description": "ver eventos da semana"},
    {"command": "aniversarios", "description": "ver aniversários de hoje"},
    {"command": "aniversarios_hoje", "description": "ver aniversários de hoje"},
    {"command": "aniversarios_semana", "description": "ver aniversários da semana"},
    {"command": "rotina", "description": "abrir painel de rotina"},
    {"command": "ajuda", "description": "listar comandos disponíveis"},
    {"command": "status", "description": "ver status do bot"},
    {"command": "debug_agenda", "description": "diagnosticar agenda"},
    {"command": "debug_aniversarios", "description": "diagnosticar aniversários"},
    {"command": "health", "description": "checar saúde do bot"},
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
        response = requests.post(
            f"{TELEGRAM_API_BASE}/bot{token}/setMyCommands",
            json={"commands": COMMANDS},
            timeout=30,
        )
        response_json = response.json()
    except requests.RequestException as exc:
        print(f"erro: falha ao chamar Telegram setMyCommands ({exc.__class__.__name__})", file=sys.stderr)
        return 1
    except ValueError:
        print("erro: Telegram retornou resposta não JSON", file=sys.stderr)
        print(response.text)
        return 1

    _print_json(response_json)
    return 0 if isinstance(response_json, dict) and response_json.get("ok") is True else 1


if __name__ == "__main__":
    sys.exit(main())
