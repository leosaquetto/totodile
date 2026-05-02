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

    if data == "agenda_semana":
        send_message(GROUP_ID, lembretes.render_week_events(), thread_id=THREADS["agenda"])
        answer_callback_query(callback_id)
        return {"ok": True, "type": "agenda_week"}

    if data == "aniversarios_semana":
        send_message(GROUP_ID, lembretes.render_week_birthdays(), thread_id=THREADS["aniversarios"])
        answer_callback_query(callback_id)
        return {"ok": True, "type": "aniversarios_week"}

    if data == "agenda_lembrar_depois":
        state = lembretes._load_state()
        state.setdefault("snoozed", {})[f"agenda:{datetime.now().date().isoformat()}"] = datetime.now().astimezone().isoformat()
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar snooze da agenda")
        answer_callback_query(callback_id, "vou lembrar depois")
        return {"ok": True, "type": "agenda_snooze"}

    return {"ok": False, "reason": "unhandled_agenda_callback", "data": data}
