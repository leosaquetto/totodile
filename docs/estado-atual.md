# Estado atual do Totodile

Última revisão: 2026-06-03.

## Runtime

- `.github/workflows/bot.yml` executa `python -m app.main` diariamente às 07h de Brasília.
- `.github/workflows/totodile-snooze.yml` roda de hora em hora entre 08h e 19h BRT para lembretes adiados.
- `.github/workflows/process-update.yml` processa um update JSON manual para debug.
- `api/telegram_webhook.py` recebe comandos e callbacks em tempo real pela Vercel.

## Entrada do Telegram

- `app/hooks/main_hook.py` processa `message`, `edited_message` e `callback_query`.
- `app/commands/router.py` roteia comandos.
- `app/callbacks/router.py` roteia callbacks por prefixo:
  - `agenda_`
  - `aniversarios_`
  - `rotina_`
  - `prep_`
  - `tarefa_`
  - `academia_`

Mensagens que não são comandos são ignoradas com segurança.

## Estado

- `app/storage.py` centraliza leitura e escrita JSON.
- Com `GITHUB_TOKEN`, o estado é lido/escrito via GitHub Contents API.
- Sem `GITHUB_TOKEN`, o estado usa os arquivos locais em `data/`.

Arquivos de dados principais:

- `data/agenda/eventos.json`
- `data/aniversarios/aniversarios.json`
- `data/lembretes/sent_state.json`
- `data/remedios/prep_state.json`
- `data/tarefas/habitos_modelo.json`
- `data/academia/treino_state.json`

## Deploy

- A Vercel precisa das envs documentadas em `docs/deploy-vercel.md`.
- O webhook real é `/api/telegram_webhook`.
- Não há polling recorrente.
