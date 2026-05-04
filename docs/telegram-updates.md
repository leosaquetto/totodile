# Telegram updates no Totodile

## Situação atual

- O workflow diário (`.github/workflows/bot.yml`) executa `python app/main.py` para envio de resumos e painéis.
- Esse fluxo **não** recebe updates em tempo real do Telegram (sem webhook/polling ativo contínuo).

## Teste manual de comandos e callbacks

Foi adicionado o workflow manual `.github/workflows/process-update.yml` com `workflow_dispatch` e input `update_json`.

Ele executa:

```bash
echo '${{ inputs.update_json }}' | python app/process_update.py
```

O script `app/process_update.py` lê JSON via stdin e chama `handle_update(update)` de `app/hooks/main_hook_stub.py`, permitindo validar manualmente:

- comandos (`/status`, `/agenda`, etc.);
- callbacks (`agenda_semana`, `aniversarios_semana`, etc.).

## Limitação para produção

Para botões/comandos funcionarem de forma real em produção, ainda será necessário um runtime contínuo com:

- webhook (endpoint público), ou
- polling (processo sempre ligado).

Até lá, o recebimento de updates segue apenas em modo de teste manual via GitHub Actions.
