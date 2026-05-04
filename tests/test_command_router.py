import unittest
from unittest.mock import patch

from app.commands.router import dispatch_command


class CommandRouterTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
