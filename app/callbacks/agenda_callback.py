from datetime import datetime

from app.modules import lembretes
from app.telegram_api import edit_message_reply_markup
from app.telegram_api_callbacks import answer_callback_query


def _answer_safe(callback_id, text=None):
    if not callback_id:
        return None
    return answer_callback_query(callback_id, text)


def _edit_buttons_safe(callback, reply_markup):
    message = callback.get("message") if isinstance(callback, dict) else None
    if not isinstance(message, dict):
        return None
    chat = message.get("chat")
    chat_id = chat.get("id") if isinstance(chat, dict) else None
    message_id = message.get("message_id")
    thread_id = message.get("message_thread_id")
    if not chat_id or not message_id:
        return None
    return edit_message_reply_markup(chat_id, message_id, reply_markup, thread_id=thread_id)


def _mark_read_flag(state, key):
    state.setdefault("read", {})[key] = datetime.now().astimezone().isoformat()


def _send_rotina_panel(data):
    if data == "rotina_tarefas_painel":
        from app.callbacks.tarefas_state import load_state
        from app.modules import tarefas_domesticas

        return tarefas_domesticas.send_panel(load_state())

    if data == "rotina_remedios_painel":
        from app.callbacks.remedios_callback import load_state
        from app.modules import remedios

        return remedios.send_prep(load_state())

    if data == "rotina_academia_painel":
        from app.callbacks.academia_callback import load_state
        from app.modules import academia

        return academia.send_academia(load_state())

    return None


def handle(callback):
    if not isinstance(callback, dict):
        return {"ok": False, "reason": "invalid_callback"}

    data = str(callback.get("data") or "")
    callback_id = callback.get("id")

    if data == "agenda_lida":
        _answer_safe(callback_id, "agenda marcada como lida")
        _edit_buttons_safe(callback, {
            "inline_keyboard": [[
                {"text": "📅 ver semana", "callback_data": "agenda_semana"},
                {"text": "📅 ver mês", "callback_data": "agenda_mes"},
            ], [
                {"text": "📅 escolher período", "callback_data": "agenda_periodo"},
            ]]
        })
        state = lembretes._load_state()
        _mark_read_flag(state, "agenda")
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar agenda lida")
        return {"ok": True, "type": "agenda_read"}

    if data == "aniversarios_lidos":
        _answer_safe(callback_id, "aniversários marcados como lidos")
        _edit_buttons_safe(callback, {
            "inline_keyboard": [[
                {"text": "🎈 ver semana", "callback_data": "aniversarios_semana"},
                {"text": "🎈 ver mês", "callback_data": "aniversarios_mes"},
            ], [
                {"text": "🎈 escolher período", "callback_data": "aniversarios_periodo"},
            ]]
        })
        state = lembretes._load_state()
        _mark_read_flag(state, "aniversarios")
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar aniversários lidos")
        return {"ok": True, "type": "aniversarios_read"}

    if data == "agenda_hoje":
        _answer_safe(callback_id)
        lembretes.send_daily_events()
        return {"ok": True, "type": "agenda_today"}

    if data == "aniversarios_hoje":
        _answer_safe(callback_id)
        lembretes.send_daily_birthdays()
        return {"ok": True, "type": "aniversarios_today"}

    if data == "agenda_semana":
        _answer_safe(callback_id)
        lembretes.send_week_events()
        return {"ok": True, "type": "agenda_week"}

    if data == "aniversarios_semana":
        _answer_safe(callback_id)
        lembretes.send_week_birthdays()
        return {"ok": True, "type": "aniversarios_week"}

    if data == "agenda_mes":
        _answer_safe(callback_id)
        lembretes.send_month_events()
        return {"ok": True, "type": "agenda_month"}

    if data == "aniversarios_mes":
        _answer_safe(callback_id)
        lembretes.send_month_birthdays()
        return {"ok": True, "type": "aniversarios_month"}

    if data == "agenda_periodo":
        _answer_safe(callback_id)
        lembretes.send_message(
            lembretes.GROUP_ID,
            "📅 quantos dias pra frente você quer ver?",
            thread_id=lembretes.THREADS["agenda"],
            reply_markup={
                "inline_keyboard": [[
                    {"text": "7 dias", "callback_data": "agenda_periodo_7"},
                    {"text": "15 dias", "callback_data": "agenda_periodo_15"},
                ], [
                    {"text": "30 dias", "callback_data": "agenda_periodo_30"},
                    {"text": "60 dias", "callback_data": "agenda_periodo_60"},
                ], [
                    {"text": "✖️ fechar", "callback_data": "agenda_fechar"},
                ]]
            }
        )
        return {"ok": True, "type": "agenda_period_prompt"}

    if data == "aniversarios_periodo":
        _answer_safe(callback_id)
        lembretes.send_message(
            lembretes.GROUP_ID,
            "🎈 quantos dias pra frente você quer ver?",
            thread_id=lembretes.THREADS["aniversarios"],
            reply_markup={
                "inline_keyboard": [[
                    {"text": "7 dias", "callback_data": "aniversarios_periodo_7"},
                    {"text": "15 dias", "callback_data": "aniversarios_periodo_15"},
                ], [
                    {"text": "30 dias", "callback_data": "aniversarios_periodo_30"},
                    {"text": "60 dias", "callback_data": "aniversarios_periodo_60"},
                ], [
                    {"text": "✖️ fechar", "callback_data": "agenda_fechar"},
                ]]
            }
        )
        return {"ok": True, "type": "aniversarios_period_prompt"}

    if data.startswith("agenda_periodo_"):
        _answer_safe(callback_id)
        days_str = data.replace("agenda_periodo_", "")
        if days_str.isdigit():
            lembretes.send_period_events(days=int(days_str))
        return {"ok": True, "type": "agenda_period"}

    if data.startswith("aniversarios_periodo_"):
        _answer_safe(callback_id)
        days_str = data.replace("aniversarios_periodo_", "")
        if days_str.isdigit():
            lembretes.send_period_birthdays(days=int(days_str))
        return {"ok": True, "type": "aniversarios_period"}

    if data == "agenda_fechar":
        _answer_safe(callback_id, "fechado")
        _edit_buttons_safe(callback, {"inline_keyboard": []})
        return {"ok": True, "type": "agenda_close"}

    if data in {"rotina_tarefas_painel", "rotina_remedios_painel", "rotina_academia_painel"}:
        _answer_safe(callback_id, "painel aberto")
        result = _send_rotina_panel(data)
        return {"ok": True, "type": "rotina_panel", "data": data, "result": result}

    if data == "menu_ajuda":
        _answer_safe(callback_id, "comandos disponíveis")
        from app.commands.agenda_commands import send_help
        send_help()
        return {"ok": True, "type": "menu_help"}

    if data == "menu_status":
        _answer_safe(callback_id, "verificando status")
        from app.commands.agenda_commands import send_status
        send_status()
        return {"ok": True, "type": "menu_status"}

    if data == "agenda_lembrar_depois":
        _answer_safe(callback_id, "vou lembrar depois")
        now = datetime.now().astimezone()
        day_key = now.date().isoformat()
        state = lembretes._load_state()
        state.setdefault("snoozed", {})[f"snooze_agenda:{day_key}"] = {
            "requested_at": now.isoformat(),
            "day": day_key
        }
        lembretes._save_json(lembretes.STATE_PATH, state, "🤖 registrar snooze da agenda")
        return {"ok": True, "type": "agenda_snooze", "day": day_key}

    _answer_safe(callback_id, "ação não reconhecida")
    return {"ok": False, "reason": "unhandled_agenda_callback", "data": data}
