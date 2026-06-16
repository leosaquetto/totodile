# Totodile — Telegram Bot
# ========================

# ─── Ngrok (túnel para webhook do Telegram) ────────────────────────
# Porta: 8443 (Hermes gateway)
# Gerenciado por launchd: sobe automático no login.
# Só use esses comandos se precisar reiniciar manualmente.

ngrok:
	ngrok http 8443 --log=stdout

ngrok-start:
	launchctl load ~/Library/LaunchAgents/local.ngrok.plist

ngrok-stop:
	launchctl unload ~/Library/LaunchAgents/local.ngrok.plist

ngrok-url:
	curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys,json; d=json.load(sys.stdin); [print(t['public_url'],'→',t['config']['addr']) for t in d.get('tunnels',[])]"

ngrok-logs:
	tail -f ~/.hermes/logs/ngrok.log

# ─── Hermes Gateway ────────────────────────────────────────────────

gw-status:
	hermes gateway status

gw-restart:
	hermes gateway restart

gw-logs:
	tail -f ~/.hermes/logs/gateway.log
