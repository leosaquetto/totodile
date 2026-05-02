# Lembrete posterior (fase 5)

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

## Limitação atual

- Nesta fase, o clique **não cria novo agendamento automático**.
- O workflow diário principal permanece inalterado.
- A execução posterior (ex.: job horário dedicado de snooze) fica para PR futura.
