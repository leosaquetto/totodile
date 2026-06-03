from app.commands import agenda_commands


COMMANDS = {
    "/agenda": agenda_commands.send_agenda_hoje,
    "/agenda_hoje": agenda_commands.send_agenda_hoje,
    "/agenda_semana": agenda_commands.send_agenda_semana,
    "/aniversarios": agenda_commands.send_aniversarios_hoje,
    "/aniversarios_hoje": agenda_commands.send_aniversarios_hoje,
    "/aniversarios_semana": agenda_commands.send_aniversarios_semana,
    "/rotina": agenda_commands.send_rotina_panel,
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


def dispatch_command(text):
    raw_text = str(text or "").strip()
    if not raw_text.startswith("/"):
        return {"ok": False, "reason": "ignored_non_command"}

    command = _normalize_command(raw_text)
    handler = COMMANDS.get(command)
    if not handler:
        result = agenda_commands.send_help()
        return {"ok": True, "reason": "unknown_command_help_sent", "command": command, "result": result}

    result = handler()
    return {"ok": True, "command": command, "result": result}
