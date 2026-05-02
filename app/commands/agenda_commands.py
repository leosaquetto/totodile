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
    text = (
        "🐊 rotina\n\n"
        "• agenda: /agenda | /agenda_semana\n"
        "• aniversários: /aniversarios | /aniversarios_semana\n"
        "• tarefas: em breve\n"
        "• remédios: em breve\n"
        "• academia: em breve"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["general"])


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
        "/ajuda"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["general"])
