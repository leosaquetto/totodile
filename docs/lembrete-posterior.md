# Lembrete posterior

Estado atual do `agenda_lembrar_depois`:

- Ao clicar em **🔁 lembrar depois**, o bot registra em `data/lembretes/sent_state.json` uma entrada em `snoozed` com chave no formato:
  - `snooze_agenda:YYYY-MM-DD`
- Para cada chave, são salvos:
  - `requested_at` (timestamp ISO)
  - `day` (data do clique)

Exemplo:

```json
{
  "snoozed": {
    "snooze_agenda:2026-05-02": {
      "requested_at": "2026-05-02T10:00:00+00:00",
      "day": "2026-05-02"
    }
  }
}
```

## Execução posterior

- O clique não cria um agendamento novo individual.
- Ele marca o dia como adiado em `snoozed`.
- O workflow `.github/workflows/totodile-snooze.yml` roda de hora em hora entre 08h e 19h BRT.
- Quando há snooze pendente para o dia, `python -m app.snooze` reenfileira a agenda no tópico correto e marca `snooze_sent_agenda:YYYY-MM-DD`.
