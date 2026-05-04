from datetime import datetime

from app.modules import lembretes
from app.telegram_api_callbacks import answer_callback_query


def _answer_safe(callback_id, text=None):
    if not callback_id:
        return None
    return answer_callback_query(callback_id, text)


def _mark_read_flag(state, key):
    state.setdefault("read", {})[key] = datetime.now().astimezone().isoformat()


def handle(callback):
    data = callback.get("data", "")
    callback_id = callback.get("id")

    if data == "agenda_lida":
        state = lembretes._load_state()
        _mark_read_flag(state, "agenda")
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar agenda lida")
        _answer_safe(callback_id, "agenda marcada como lida")
        return {"ok": True, "type": "agenda_read"}

    if data == "aniversarios_lidos":
        state = lembretes._load_state()
        _mark_read_flag(state, "aniversarios")
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar aniversários lidos")
        _answer_safe(callback_id, "aniversários marcados como lidos")
        return {"ok": True, "type": "aniversarios_read"}

    if data == "agenda_hoje":
        lembretes.send_daily_events()
        _answer_safe(callback_id)
        return {"ok": True, "type": "agenda_today"}

    if data == "aniversarios_hoje":
        lembretes.send_daily_birthdays()
        _answer_safe(callback_id)
        return {"ok": True, "type": "aniversarios_today"}

    if data == "agenda_semana":
        lembretes.send_week_events()
        _answer_safe(callback_id)
        return {"ok": True, "type": "agenda_week"}

    if data == "aniversarios_semana":
        lembretes.send_week_birthdays()
        _answer_safe(callback_id)
        return {"ok": True, "type": "aniversarios_week"}

    if data in {"rotina_tarefas_painel", "rotina_remedios_painel", "rotina_academia_painel"}:
        _answer_safe(callback_id, "painel em breve")
        return {"ok": True, "type": "rotina_em_breve", "data": data}

    if data == "agenda_lembrar_depois":
        now = datetime.now().astimezone()
        day_key = now.date().isoformat()
        state = lembretes._load_state()
        state.setdefault("snoozed", {})[f"snooze_agenda:{day_key}"] = {
            "requested_at": now.isoformat(),
            "day": day_key
        }
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar snooze da agenda")
        _answer_safe(callback_id, "vou lembrar depois")
        return {"ok": True, "type": "agenda_snooze", "day": day_key}

    return {"ok": False, "reason": "unhandled_agenda_callback", "data": data}
