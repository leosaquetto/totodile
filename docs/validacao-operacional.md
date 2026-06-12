# Validação operacional

Checklist curto para validar o bot após mudanças.

## Código

```bash
python -m compileall app api scripts
python -m unittest discover -s tests
printf '%s' '{"update_id":1,"message":{"message_id":1,"text":"oi"}}' | python -m app.process_update
```

Objetivo:

- detectar erro de sintaxe;
- validar testes unitários;
- confirmar que update sem comando é ignorado sem bater no Telegram.

## Workflows

- Rodar `totodile-smoke-check`.
- Rodar `totodile-bot` manualmente e confirmar envio nos tópicos `agenda` e `aniversarios`.
- Rodar `totodile-snooze` manualmente quando houver snooze no dia.
- Rodar `process-update` com JSON fake.

## Webhook

Validar na URL pública da Vercel:

- `GET /api/health` retorna `200` com `ok: true` e booleanos de configuração.
- `GET /api/telegram_webhook` retorna `405`.
- `POST` com JSON inválido retorna `400`.
- `POST` com secret inválido retorna `403`.
- `POST` com payload válido retorna JSON.

## Checagem pós-deploy em 5 minutos

1. Rode `totodile-smoke-check`.
2. Abra `https://SEU-DOMINIO.vercel.app/api/health` e confirme `ok: true`.
3. Execute `TOKEN_TOTODILE=... python scripts/get_telegram_webhook_info.py`.
4. Confirme `pending_update_count` baixo e `last_error_message` vazio.
5. Envie `/health` no Telegram e confirme a resposta no tópico geral.

## Telegram

Testar comandos:

- `/agenda`
- `/agenda_hoje`
- `/agenda_semana`
- `/aniversarios`
- `/aniversarios_hoje`
- `/aniversarios_semana`
- `/rotina`
- `/ajuda`
- `/status`
- `/debug_agenda`
- `/debug_aniversarios`
- `/health`

Testar botões:

- `✅ li agenda`
- `📅 ver semana`
- `🔁 lembrar depois`
- `✅ li aniversários`
- `🎈 ver semana`
- botões de tarefas;
- botões de remédios;
- botões de academia.

## Estado

Com `GITHUB_TOKEN` configurado, confirmar commits/updates em:

- `data/lembretes/sent_state.json`
- `data/remedios/prep_state.json`
- `data/tarefas/habitos_modelo.json`
- `data/academia/treino_state.json`

Sem `GITHUB_TOKEN`, confirmar escrita local apenas em desenvolvimento.

## Checklist para corpo da PR

Incluir na descrição da PR:

- arquivos alterados;
- como testar o workflow diário `totodile-bot`;
- como testar `process-update.yml`;
- como configurar envs na Vercel;
- como registrar webhook com `scripts/set_telegram_webhook.py`;
- como checar `getWebhookInfo` com `scripts/get_telegram_webhook_info.py`;
- quais comandos foram validados;
- limitações conhecidas;
- itens externos pendentes, se houver.
