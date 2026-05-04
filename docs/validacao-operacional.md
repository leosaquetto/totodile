# Validação operacional (fase 11)

Checklist curto para validar o bot após mudanças.

## 1) Integridade de código
Execute localmente:

```bash
python -m compileall app
```

Objetivo: detectar erro de sintaxe antes de workflow/produção.

## 2) Fluxo diário
- Rodar workflow manual (`workflow_dispatch`).
- Confirmar envio em:
  - tópico agenda
  - tópico aniversários

## 3) Botões dos resumos
No Telegram, validar:
- `✅ li agenda`
- `📅 ver semana`
- `🔁 lembrar depois`
- `✅ li aniversários`
- `🎈 ver semana`

## 4) Comandos
Testar:
- `/agenda`, `/agenda_semana`
- `/aniversarios`, `/aniversarios_semana`
- `/rotina`, `/ajuda`
- `/status`, `/debug_agenda`, `/debug_aniversarios`

## 5) Estado
Verificar `data/lembretes/sent_state.json`:
- `sent`
- `read`
- `snoozed`
- `last_daily_summary`

## 6) Scriptable
- Executar exportador no iPhone.
- Confirmar atualização de:
  - `data/agenda/eventos.json`
  - `data/aniversarios/aniversarios.json`
- Confirmar metadados: `exportedAt`, `source`, `count`, `timezone`, `branch`, `items`.
