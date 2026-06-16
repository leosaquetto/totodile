# Totodile — Telegram Bot
# ========================

default:
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "── Ngrok ──"
	@echo "  make ngrok        Iniciar ngrok manual (porta 8443)"
	@echo "  make ngrok-start  Ativar launchd (auto-start no login)"
	@echo "  make ngrok-stop   Parar ngrok do launchd"
	@echo "  make ngrok-url    Mostrar URL pública do túnel"
	@echo "  make ngrok-logs   Seguir logs do ngrok"
	@echo ""
	@echo "── Gateway ──"
	@echo "  make gw-status    Status do Hermes gateway"
	@echo "  make gw-restart   Reiniciar gateway"
	@echo "  make gw-logs      Seguir logs do gateway"

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
