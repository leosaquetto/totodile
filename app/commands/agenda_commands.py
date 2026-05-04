from app.config import GROUP_ID, BOT_TOKEN
from app.constants import THREADS
from app.modules import lembretes
from app.telegram_api import send_message


def send_agenda_hoje():
    return lembretes.send_daily_events()


def send_agenda_semana():
    return lembretes.send_week_events()


def send_aniversarios_hoje():
    return lembretes.send_daily_birthdays()


def send_aniversarios_semana():
    return lembretes.send_week_birthdays()


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
        "/debug_aniversarios\n"
        "/health"
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


def send_health():
    now = lembretes._now()
    state = lembretes._load_state()
    text = (
        "🧪 health\n\n"
        f"token: {'ok' if BOT_TOKEN else 'ausente'}\n"
        f"group_id: {'ok' if GROUP_ID else 'ausente'}\n"
        f"state.sent: {len(state.get('sent', {}))}\n"
        f"state.read: {len(state.get('read', {}))}\n"
        f"state.snoozed: {len(state.get('snoozed', {}))}\n"
        f"agora: {now.isoformat()}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["general"])
