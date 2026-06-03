# Agenda e aniversários no Totodile

## Dados usados
- `data/agenda/eventos.json`
- `data/aniversarios/aniversarios.json`
- `data/lembretes/sent_state.json`

## Fluxo diário
- O workflow diário executa `python -m app.main`.
- O módulo `app/modules/lembretes.py` chama `send_due_reminders()`.
- O bot envia resumo diário para:
  - tópico `agenda`
  - tópico `aniversarios`

## Botões nos resumos
### Agenda
- `✅ li agenda` → `agenda_lida`
- `📅 ver semana` → `agenda_semana`
- `🔁 lembrar depois` → `agenda_lembrar_depois`

### Aniversários
- `✅ li aniversários` → `aniversarios_lidos`
- `🎈 ver semana` → `aniversarios_semana`

## Callback routing
- `app/callbacks/router.py` roteia:
  - `agenda_`
  - `aniversarios_`
  - `rotina_`
- Handler: `app/callbacks/agenda_callback.py`

## Lembrete posterior (snooze)
- Ao clicar `agenda_lembrar_depois`, o estado salva em `sent_state.json` em `snoozed` com chave:
  - `snooze_agenda:YYYY-MM-DD`
- Exemplo de valor:
  - `requested_at` (ISO)
  - `day` (YYYY-MM-DD)

## Teste rápido via workflow_dispatch
1. Abra **Actions** no GitHub.
2. Execute o workflow do bot manualmente com **Run workflow**.
3. Verifique no Telegram os tópicos de agenda e aniversários.
