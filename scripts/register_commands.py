#!/usr/bin/env python3
"""Register slash commands in Telegram via Bot API."""
import os
import sys
import json
import urllib.request
import urllib.error

BOT_TOKEN = os.getenv("TOKEN_TOTODILE")
if not BOT_TOKEN:
    print("ERRO: TOKEN_TOTODILE nao definido", file=sys.stderr)
    sys.exit(1)

COMMANDS = [
    {"command": "agenda", "description": "📅 Eventos de hoje"},
    {"command": "agenda_hoje", "description": "📅 Eventos de hoje"},
    {"command": "agenda_semana", "description": "📅 Próximos 7 dias"},
    {"command": "agenda_mes", "description": "📅 Visão do mês"},
    {"command": "aniversarios", "description": "🎈 Aniversariantes de hoje"},
    {"command": "aniversarios_hoje", "description": "🎈 Aniversariantes de hoje"},
    {"command": "aniversarios_semana", "description": "🎈 Próximos 7 dias"},
    {"command": "aniversarios_mes", "description": "🎈 Visão do mês"},
    {"command": "menu", "description": "🐊 Menu principal"},
    {"command": "rotina", "description": "🏠 Tarefas, remédios e academia"},
    {"command": "ajuda", "description": "❓ Lista completa de comandos"},
    {"command": "status", "description": "🩺 Status do bot"},
]

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setMyCommands"
payload = json.dumps({"commands": COMMANDS}).encode()

req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("ok"):
        print(f"\n✅ {len(COMMANDS)} comandos registrados com sucesso!")
    else:
        print(f"\n❌ Erro: {result}")
        sys.exit(1)
except urllib.error.HTTPError as e:
    print(f"❌ HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"❌ {e}", file=sys.stderr)
    sys.exit(1)
