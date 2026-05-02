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
}


def _normalize_command(text):
    raw = str(text or "").strip().split()[0]
    return raw.split("@")[0].lower()


def dispatch_command(text):
    command = _normalize_command(text)
    handler = COMMANDS.get(command)
    if not handler:
        agenda_commands.send_help()
        return {"ok": False, "reason": "unknown_command", "command": command}

    handler()
    return {"ok": True, "command": command}
