## Resumo

<!-- Descreva o objetivo e o comportamento alterado. -->

## Arquivos alterados

<!-- Liste os arquivos principais e a responsabilidade de cada mudança. -->

## Como testar

### Workflow diário

1. Abra Actions > `totodile-bot`.
2. Execute `workflow_dispatch`.
3. Confirme o envio nos tópicos esperados.

### Process update

1. Abra Actions > `process-update`.
2. Execute com:

```json
{"update_id":1,"message":{"message_id":1,"text":"oi"}}
```

3. Confirme que a mensagem sem comando foi ignorada com segurança.

### Validação local

```bash
python -m compileall app api scripts
python -m unittest discover -s tests
printf '%s' '{"update_id":1,"message":{"message_id":1,"text":"oi"}}' | python -m app.process_update
```

## Vercel

Envs necessárias:

- `TOKEN_TOTODILE`
- `ID_CENTRAL_TOTODILE`
- `GITHUB_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`

Registrar webhook:

```bash
TOKEN_TOTODILE=... TELEGRAM_WEBHOOK_URL=https://SEU-DOMINIO.vercel.app/api/telegram_webhook TELEGRAM_WEBHOOK_SECRET=... python scripts/set_telegram_webhook.py
```

Checar webhook:

```bash
TOKEN_TOTODILE=... python scripts/get_telegram_webhook_info.py
```

## Comandos validados

- [ ] `/agenda`
- [ ] `/agenda_hoje`
- [ ] `/agenda_semana`
- [ ] `/aniversarios`
- [ ] `/aniversarios_hoje`
- [ ] `/aniversarios_semana`
- [ ] `/rotina`
- [ ] `/ajuda`
- [ ] `/status`
- [ ] `/debug_agenda`
- [ ] `/debug_aniversarios`
- [ ] `/health`

## Política de retry do Telegram

O webhook retorna `200 {"ok": false, "error": "internal_error"}` depois de logar uma exceção interna com segurança. A decisão evita que o Telegram reenvie indefinidamente um update que falhou por um erro determinístico.

## Limitações conhecidas

<!-- Liste limitações ou escreva "Nenhuma conhecida". -->

## Pendências externas

<!-- Liste configurações/deploys/secrets pendentes ou escreva "Nenhuma". -->
