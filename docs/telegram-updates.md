# Telegram updates no Totodile

## Papéis dos runtimes

- `.github/workflows/bot.yml`: envia o resumo diário às 07h de Brasília com `python -m app.main`.
- `.github/workflows/process-update.yml`: processa manualmente um update JSON para debug.
- Webhook Vercel: recebe comandos e botões em tempo real em `/api/telegram_webhook`.

Não existe workflow recorrente de polling. Depois que o webhook estiver registrado, o Telegram chama a Vercel automaticamente para comandos e callbacks.

## Fluxo do webhook

1. O Telegram envia `POST /api/telegram_webhook`.
2. O endpoint valida JSON e, se configurado, o header `X-Telegram-Bot-Api-Secret-Token`.
3. O endpoint chama `handle_update(update)` em `app/hooks/main_hook.py`.
4. O hook roteia `callback_query` para `app/callbacks/router.py`.
5. O hook roteia `message.text` e `edited_message.text` para `app/commands/router.py`.
6. Mensagens sem comando são ignoradas com segurança.

Respostas esperadas:

- método diferente de `POST`: `405`.
- JSON inválido: `400`.
- payload que não é objeto: `400`.
- secret inválido: `403`.
- sucesso: `200 {"ok": true, "result": ...}`.
- erro interno do handler: `200 {"ok": false, "error": "internal_error"}`.

O erro interno retorna `200` para evitar que o Telegram reenfileire o mesmo update indefinidamente. O erro é logado sem expor token.

## Teste manual de update

O workflow manual `.github/workflows/process-update.yml` recebe `update_json` e executa o hook localmente.

Exemplo de JSON seguro para testar ignore de mensagem comum:

```json
{"update_id":1,"message":{"message_id":1,"text":"oi"}}
```

Teste local equivalente:

```bash
printf '%s' '{"update_id":1,"message":{"message_id":1,"text":"oi"}}' | python -m app.process_update
```

Para testar comando real, use um ambiente com `TOKEN_TOTODILE` e `ID_CENTRAL_TOTODILE`, porque o handler vai tentar responder no Telegram.

## Updates aceitos

Ao registrar o webhook, use:

```json
["message", "edited_message", "callback_query"]
```
