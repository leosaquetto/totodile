import os

from app.config import GROUP_ID, BOT_TOKEN
from app.constants import THREADS
from app.modules import lembretes
from app.telegram_api import send_message


def _chat_id(kwargs):
    return kwargs.get("chat_id") or GROUP_ID


def _thread_id(kwargs, thread_key):
    if kwargs.get("thread_id"):
        return kwargs["thread_id"]
    return THREADS.get(thread_key)


def send_agenda_hoje(**kwargs):
    return lembretes.send_daily_events()


def send_agenda_semana(**kwargs):
    return lembretes.send_week_events()


def send_aniversarios_hoje(**kwargs):
    return lembretes.send_daily_birthdays()


def send_aniversarios_semana(**kwargs):
    return lembretes.send_week_birthdays()


def send_agenda_mes(**kwargs):
    return lembretes.send_month_events()


def send_aniversarios_mes(**kwargs):
    return lembretes.send_month_birthdays()


def send_rotina_panel(**kwargs):
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


def send_menu(**kwargs):
    chat_id = _chat_id(kwargs)
    text = '🐊 Totodile\n\nescolha uma opção:'
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🗓️ hoje", "callback_data": "agenda_hoje"},
                {"text": "📅 semana", "callback_data": "agenda_semana"},
                {"text": "📆 mês", "callback_data": "agenda_mes"},
            ],
            [
                {"text": "🎈 aniv. hoje", "callback_data": "aniversarios_hoje"},
                {"text": "🎈 aniv. semana", "callback_data": "aniversarios_semana"},
                {"text": "🎈 aniv. mês", "callback_data": "aniversarios_mes"},
            ],
            [
                {"text": "🏠 tarefas", "callback_data": "rotina_tarefas_painel"},
                {"text": "💊 remédios", "callback_data": "rotina_remedios_painel"},
                {"text": "🏋️ academia", "callback_data": "rotina_academia_painel"},
            ],
            [
                {"text": "ℹ️ ajuda", "callback_data": "menu_ajuda"},
                {"text": "🩺 status", "callback_data": "menu_status"},
            ],
        ]
    }
    return send_message(
        chat_id, text, thread_id=kwargs.get("thread_id"), reply_markup=reply_markup
    )


def send_help(**kwargs):
    chat_id = _chat_id(kwargs)
    text = "\n".join([
        "🤖 comandos disponíveis",
        "",
        "/menu — menu principal",
        "/agenda — eventos de hoje",
        "/agenda_semana — eventos da semana",
        "/agenda_mes — eventos do mês",
        "/aniversarios — aniversários de hoje",
        "/aniversarios_semana — aniversários da semana",
        "/aniversarios_mes — aniversários do mês",
        "/rotina — painel de tarefas, remédios, academia",
        "/ajuda — esta lista",
        "/status — status do bot",
    ])
    return send_message(chat_id, text, thread_id=kwargs.get("thread_id"))


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


def send_status(**kwargs):
    chat_id = _chat_id(kwargs)
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
    return send_message(chat_id, text, thread_id=kwargs.get("thread_id"))


def send_debug_agenda(**kwargs):
    now = lembretes._now()
    events = lembretes._events_between(now, 30)
    text = (
        "🐞 debug agenda\n\n"
        f"eventos carregados (30 dias): {len(events)}\n"
        f"próximo evento: {_next_event_line()}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["agenda"])


def send_debug_aniversarios(**kwargs):
    now = lembretes._now()
    birthdays = lembretes._birthdays_between(now, 30)
    text = (
        "🐞 debug aniversários\n\n"
        f"aniversários carregados (30 dias): {len(birthdays)}\n"
        f"próximo aniversário: {_next_birthday_line()}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["aniversarios"])


def send_health(**kwargs):
    now = lembretes._now()
    state = lembretes._load_state()
    github_token = os.getenv("GITHUB_TOKEN")
    text = (
        "🧪 health\n\n"
        "configuração:\n"
        f"- token Telegram: {'ok' if BOT_TOKEN else 'ausente'}\n"
        f"- grupo Telegram: {'ok' if GROUP_ID else 'ausente'}\n"
        f"- GitHub storage: {'ok' if github_token else 'modo local'}\n\n"
        "estado:\n"
        f"state.sent: {len(state.get('sent', {}))}\n"
        f"state.read: {len(state.get('read', {}))}\n"
        f"state.snoozed: {len(state.get('snoozed', {}))}\n"
        f"agora: {now.isoformat()}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["general"])
