# Estado atual do Totodile (Fase 1 - auditoria)

Data da auditoria: 2026-05-02 (UTC)

## Base de trabalho
- Branch local atual: `work`.
- Observação importante para as próximas PRs: como a `bootstrap-totodile` já foi mergeada, a base recomendada para novas branches é a `main` do repositório `leosaquetto/totodile`.

## Arquivos inspecionados
- `app/main.py`
- `app/modules/lembretes.py`
- `app/callbacks/router_stub.py`
- `app/hooks/main_hook_stub.py`
- `app/telegram_api.py`
- `app/telegram_api_callbacks.py`
- `app/constants.py`
- `.github/workflows/bot.yml`
- `ios_scriptable/exportar_agenda_aniversarios.js`

## Callbacks já existentes
Pelo roteador atual (`app/callbacks/router_stub.py`), já existem estes prefixos tratados:
- `prep_` → `app/callbacks/remedios_callback.py`
- `tarefa_` → `app/callbacks/tarefas_callback.py`
- `academia_` → `app/callbacks/academia_callback.py`

Ainda não há roteamento para:
- `agenda_`
- `aniversarios_`

## O bot hoje processa o quê?
### Envio agendado
Sim. O workflow `.github/workflows/bot.yml` executa `python app/main.py` diariamente em:
- `0 10 * * *` (10:00 UTC, 07:00 em Brasília).

No `app/main.py`, o fluxo atual chama:
- `lembretes.send_due_reminders()`
- `remedios.send_prep(...)`
- `tarefas_domesticas.send_panel(...)`
- `academia.send_academia(...)`

### Callbacks do Telegram
Parcialmente sim.
- O `app/hooks/main_hook_stub.py` processa apenas `update.callback_query` e despacha para `router_stub.dispatch(...)`.
- Ou seja, já existe suporte para callbacks (botões), mas somente para os prefixos hoje roteados.

### Mensagens de texto/comandos
Não no hook atual.
- O `main_hook_stub.py` não trata `message.text`.
- Portanto, comandos como `/agenda` ou `/ajuda` ainda não são processados nesse ponto de entrada atual.

## Observações relevantes para próximas fases
- `app/modules/lembretes.py` já possui funções de render semanal prontas:
  - `render_week_birthdays`
  - `render_week_events`
  - e também `send_week_birthdays` / `send_week_events`.
- `send_message(...)` em `app/telegram_api.py` já aceita `reply_markup`, facilitando incluir botões nos resumos diários.
- O exportador `ios_scriptable/exportar_agenda_aniversarios.js` ainda está com branch padrão `bootstrap-totodile`, que deve ser revisada em PR futura dedicada para alinhar com `main`.
