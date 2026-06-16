# Deploy Vercel

## Endpoint

O webhook real fica em:

```text
/api/telegram_webhook
```

O endpoint público de saúde fica em:

```text
/api/health
```

Em produção:

```text
https://SEU-DOMINIO.vercel.app/api/telegram_webhook
```

O endpoint é uma Python Function simples da Vercel, sem Flask/FastAPI.

`GET /api/health` retorna apenas booleanos de configuração (`has_token`, `has_group_id`, `has_github_token`) e timestamp. Ele não expõe token, secret, group id ou payload do Telegram.

O estado em produção usa GitHub Contents API via `GITHUB_TOKEN`. Sem essa env, a função cai para arquivo local, o que só é adequado em desenvolvimento.

`requirements.txt` inclui `tzdata` para garantir que `ZoneInfo("America/Sao_Paulo")` funcione mesmo em runtimes sem banco de fusos do sistema.

## Envs da Vercel

Configure na Vercel:

```text
TOKEN_TOTODILE
ID_CENTRAL_TOTODILE
GITHUB_TOKEN
TELEGRAM_WEBHOOK_SECRET
TOTODILE_ALLOWED_CHATS
```

`TELEGRAM_WEBHOOK_SECRET` é usado para validar o header `X-Telegram-Bot-Api-Secret-Token`. Se a env estiver definida e o header vier diferente, o webhook responde `403`.

`TOTODILE_ALLOWED_CHATS` é uma lista de IDs de chat separados por vírgula (ex: `-1001234567890,987654321`). Se definida, apenas mensagens desses chats são processadas — qualquer outro remetente é ignorado silenciosamente. Se não definida, todos os chats são aceitos (comportamento antigo).

## Registrar webhook

Use a URL pública da Vercel:

```bash
TOKEN_TOTODILE=... TELEGRAM_WEBHOOK_URL=https://SEU-DOMINIO.vercel.app/api/telegram_webhook TELEGRAM_WEBHOOK_SECRET=... python scripts/set_telegram_webhook.py
```

O script chama `setWebhook` com:

```json
{
  "allowed_updates": ["message", "edited_message", "callback_query"],
  "drop_pending_updates": false
}
```

Se `TELEGRAM_WEBHOOK_SECRET` estiver preenchido, o script também envia `secret_token`.

## Checar webhook

```bash
TOKEN_TOTODILE=... python scripts/get_telegram_webhook_info.py
```

O script destaca:

- `url`
- `pending_update_count`
- `last_error_date`
- `last_error_message`
- `allowed_updates`

## Remover webhook para debug

Por padrão, não descarta updates pendentes:

```bash
TOKEN_TOTODILE=... python scripts/delete_telegram_webhook.py
```

Para descartar pendências explicitamente:

```bash
TOKEN_TOTODILE=... python scripts/delete_telegram_webhook.py --drop-pending-updates
```

## Workflows

- `bot.yml`: rotina diária às 07h de Brasília.
- `process-update.yml`: debug manual de update JSON.
- Webhook Vercel: comandos e botões em tempo real.

## Smoke pós-deploy

Depois de um deploy, valide:

```bash
curl -s https://SEU-DOMINIO.vercel.app/api/health
TOKEN_TOTODILE=... python scripts/get_telegram_webhook_info.py
```

O `health` deve retornar `ok: true` e `getWebhookInfo` não deve mostrar `last_error_message`.
