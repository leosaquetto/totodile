import unittest
from unittest.mock import patch

from app.commands.router import COMMANDS, dispatch_command

REQUIRED_COMMANDS = {
    "/agenda",
    "/agenda_hoje",
    "/agenda_semana",
    "/aniversarios",
    "/aniversarios_hoje",
    "/aniversarios_semana",
    "/rotina",
    "/ajuda",
    "/status",
    "/debug_agenda",
    "/debug_aniversarios",
    "/health",
}

EXPECTED_HANDLERS = {
    "/agenda": "send_agenda_hoje",
    "/agenda_hoje": "send_agenda_hoje",
    "/agenda_semana": "send_agenda_semana",
    "/aniversarios": "send_aniversarios_hoje",
    "/aniversarios_hoje": "send_aniversarios_hoje",
    "/aniversarios_semana": "send_aniversarios_semana",
    "/rotina": "send_rotina_panel",
    "/ajuda": "send_help",
    "/status": "send_status",
    "/debug_agenda": "send_debug_agenda",
    "/debug_aniversarios": "send_debug_aniversarios",
    "/health": "send_health",
}


class CommandRouterTest(unittest.TestCase):
    def test_all_required_commands_are_registered(self):
        self.assertEqual(set(COMMANDS), REQUIRED_COMMANDS)

    def test_required_commands_map_to_expected_handlers(self):
        self.assertEqual(
            {command: handler.__name__ for command, handler in COMMANDS.items()},
            EXPECTED_HANDLERS,
        )

    @patch("app.commands.agenda_commands.send_help")
    def test_ignore_non_command(self, mock_help):
        result = dispatch_command("oi")
        self.assertEqual(result.get("reason"), "ignored_non_command")
        mock_help.assert_not_called()

    @patch("app.modules.lembretes.send_daily_events")
    def test_dispatch_known_command(self, mock_send_daily_events):
        result = dispatch_command("/agenda")
        self.assertTrue(result.get("ok"))
        mock_send_daily_events.assert_called_once()

    @patch("app.commands.agenda_commands.send_help", return_value={"ok": True})
    def test_unknown_command_sends_help(self, mock_help):
        result = dispatch_command("/nao_existe")

        self.assertTrue(result["ok"])
        self.assertEqual(result["reason"], "unknown_command_help_sent")
        mock_help.assert_called_once()

    @patch("app.modules.lembretes.send_daily_events")
    def test_bot_username_suffix_is_ignored(self, mock_send_daily_events):
        result = dispatch_command("/agenda@totodile_bot")

        self.assertTrue(result["ok"])
        self.assertEqual(result["command"], "/agenda")
        mock_send_daily_events.assert_called_once()


if __name__ == "__main__":
    unittest.main()
