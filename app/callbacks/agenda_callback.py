from datetime import datetime

from app.config import GROUP_ID
from app.constants import THREADS
from app.modules import lembretes
from app.telegram_api import send_message
from app.telegram_api_callbacks import answer_callback_query


def _mark_read_flag(state, key):
    state.setdefault("read", {})[key] = datetime.now().astimezone().isoformat()


def handle(callback):
    data = callback.get("data", "")
    callback_id = callback.get("id")

    if data == "agenda_lida":
        state = lembretes._load_state()
        _mark_read_flag(state, "agenda")
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar agenda lida")
        answer_callback_query(callback_id, "agenda marcada como lida")
        return {"ok": True, "type": "agenda_read"}

    if data == "aniversarios_lidos":
        state = lembretes._load_state()
        _mark_read_flag(state, "aniversarios")
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar aniversários lidos")
        answer_callback_query(callback_id, "aniversários marcados como lidos")
        return {"ok": True, "type": "aniversarios_read"}

    if data == "agenda_hoje":
        text = lembretes.render_daily_events() or "🗓️ agenda de hoje\n\nnenhum compromisso para hoje."
        send_message(GROUP_ID, text, thread_id=THREADS["agenda"])
        answer_callback_query(callback_id)
        return {"ok": True, "type": "agenda_today"}

    if data == "aniversarios_hoje":
        text = lembretes.render_daily_birthdays() or "🎈 aniversários de hoje\n\nnenhum aniversário para hoje."
        send_message(GROUP_ID, text, thread_id=THREADS["aniversarios"])
        answer_callback_query(callback_id)
        return {"ok": True, "type": "aniversarios_today"}

    if data == "agenda_semana":
        send_message(GROUP_ID, lembretes.render_week_events(), thread_id=THREADS["agenda"])
        answer_callback_query(callback_id)
        return {"ok": True, "type": "agenda_week"}

    if data == "aniversarios_semana":
        send_message(GROUP_ID, lembretes.render_week_birthdays(), thread_id=THREADS["aniversarios"])
        answer_callback_query(callback_id)
        return {"ok": True, "type": "aniversarios_week"}

    if data in {"rotina_tarefas_painel", "rotina_remedios_painel", "rotina_academia_painel"}:
        answer_callback_query(callback_id, "painel em breve")
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
        answer_callback_query(callback_id, "vou lembrar depois")
        return {"ok": True, "type": "agenda_snooze", "day": day_key}

    return {"ok": False, "reason": "unhandled_agenda_callback", "data": data}
