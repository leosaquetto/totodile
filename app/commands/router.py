from app.commands import agenda_commands


COMMANDS = {
    "/agenda": agenda_commands.send_agenda_hoje,
    "/agenda_hoje": agenda_commands.send_agenda_hoje,
    "/agenda_semana": agenda_commands.send_agenda_semana,
    "/agenda_mes": agenda_commands.send_agenda_mes,
    "/aniversarios": agenda_commands.send_aniversarios_hoje,
    "/aniversarios_hoje": agenda_commands.send_aniversarios_hoje,
    "/aniversarios_semana": agenda_commands.send_aniversarios_semana,
    "/aniversarios_mes": agenda_commands.send_aniversarios_mes,
    "/rotina": agenda_commands.send_rotina_panel,
    "/menu": agenda_commands.send_menu,
    "/start": agenda_commands.send_menu,
    "/ajuda": agenda_commands.send_help,
    "/status": agenda_commands.send_status,
    "/debug_agenda": agenda_commands.send_debug_agenda,
    "/debug_aniversarios": agenda_commands.send_debug_aniversarios,
    "/health": agenda_commands.send_health,
}


def _normalize_command(text):
    parts = str(text or "").strip().split()
    if not parts:
        return ""
    raw = parts[0]
    return raw.split("@")[0].lower()


def _get_chat_context(message):
    if not isinstance(message, dict):
        return {}
    chat = message.get("chat") if isinstance(message.get("chat"), dict) else None
    chat_id = chat.get("id") if chat else None
    thread_id = message.get("message_thread_id")
    ctx = {}
    if chat_id:
        ctx["chat_id"] = chat_id
    if thread_id:
        ctx["thread_id"] = thread_id
    return ctx


def dispatch_command(text, message=None):
    raw_text = str(text or "").strip()
    if not raw_text.startswith("/"):
        return {"ok": False, "reason": "ignored_non_command"}

    command = _normalize_command(raw_text)
    handler = COMMANDS.get(command)
    if not handler:
        result = agenda_commands.send_help(**_get_chat_context(message))
        return {"ok": True, "reason": "unknown_command_help_sent", "command": command, "result": result}

    result = handler(**_get_chat_context(message))
    return {"ok": True, "command": command, "result": result}
