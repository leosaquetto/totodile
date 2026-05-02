from app.config import GROUP_ID
from app.constants import THREADS
from app.modules import lembretes
from app.telegram_api import send_message


def send_agenda_hoje():
    text = lembretes.render_daily_events() or "🗓️ agenda de hoje\n\nnenhum compromisso para hoje."
    return send_message(GROUP_ID, text, thread_id=THREADS["agenda"])


def send_agenda_semana():
    return send_message(GROUP_ID, lembretes.render_week_events(), thread_id=THREADS["agenda"])


def send_aniversarios_hoje():
    text = lembretes.render_daily_birthdays() or "🎈 aniversários de hoje\n\nnenhum aniversário para hoje."
    return send_message(GROUP_ID, text, thread_id=THREADS["aniversarios"])


def send_aniversarios_semana():
    return send_message(GROUP_ID, lembretes.render_week_birthdays(), thread_id=THREADS["aniversarios"])


def send_rotina_panel():
    text = "🐊 rotina\n\nuse os botões para acessar os módulos:"
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🗓️ agenda hoje", "callback_data": "agenda_hoje"},
                {"text": "📅 agenda semana", "callback_data": "agenda_semana"}
            ],
            [
                {"text": "🎈 aniversários hoje", "callback_data": "aniversarios_hoje"},
                {"text": "🎈 aniversários semana", "callback_data": "aniversarios_semana"}
            ],
            [
                {"text": "🏠 tarefas", "callback_data": "rotina_tarefas_painel"},
                {"text": "💊 remédios", "callback_data": "rotina_remedios_painel"},
                {"text": "🏋️ academia", "callback_data": "rotina_academia_painel"}
            ]
        ]
    }
    return send_message(GROUP_ID, text, thread_id=THREADS["general"], reply_markup=reply_markup)


def send_help():
    text = (
        "🤖 comandos disponíveis\n\n"
        "/agenda\n"
        "/agenda_hoje\n"
        "/agenda_semana\n"
        "/aniversarios\n"
        "/aniversarios_hoje\n"
        "/aniversarios_semana\n"
        "/rotina\n"
        "/ajuda\n"
        "/status\n"
        "/debug_agenda\n"
        "/debug_aniversarios"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["general"])


def _next_event_line():
    now = lembretes._now()
    events = lembretes._events_between(now, 30)
    if not events:
        return "nenhum próximo evento"
    item = events[0]
    return f"{item['date']:%d/%m %H:%M} — {item['title']}"


def _next_birthday_line():
    now = lembretes._now()
    birthdays = lembretes._birthdays_between(now, 30)
    if not birthdays:
        return "nenhum próximo aniversário"
    item = birthdays[0]
    return f"{item['date']:%d/%m} — {item['title']}"


def send_status():
    now = lembretes._now()
    state = lembretes._load_state()
    events = lembretes._events_between(now, 30)
    birthdays = lembretes._birthdays_between(now, 30)

    text = (
        "🩺 status do bot\n\n"
        f"último resumo diário: {state.get('last_daily_summary') or 'não registrado'}\n"
        f"eventos carregados (30 dias): {len(events)}\n"
        f"aniversários carregados (30 dias): {len(birthdays)}\n"
        f"read: {len(state.get('read', {}))} | snoozed: {len(state.get('snoozed', {}))}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["general"])


def send_debug_agenda():
    now = lembretes._now()
    events = lembretes._events_between(now, 30)
    text = (
        "🐞 debug agenda\n\n"
        f"eventos carregados (30 dias): {len(events)}\n"
        f"próximo evento: {_next_event_line()}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["agenda"])


def send_debug_aniversarios():
    now = lembretes._now()
    birthdays = lembretes._birthdays_between(now, 30)
    text = (
        "🐞 debug aniversários\n\n"
        f"aniversários carregados (30 dias): {len(birthdays)}\n"
        f"próximo aniversário: {_next_birthday_line()}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["aniversarios"])
