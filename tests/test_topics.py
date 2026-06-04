import unittest
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from app.commands import agenda_commands
from app.constants import THREADS
from app.modules import academia, lembretes, remedios, tarefas_domesticas


class TopicTest(unittest.TestCase):
    def test_general_commands_do_not_send_message_thread_id(self):
        now = datetime(2026, 6, 3, 12, tzinfo=ZoneInfo("America/Sao_Paulo"))
        state = {"sent": {}, "read": {}, "snoozed": {}, "last_daily_summary": None}

        with patch.object(agenda_commands, "send_message", return_value={"ok": True}) as send_message:
            with patch.object(agenda_commands.lembretes, "_now", return_value=now):
                with patch.object(agenda_commands.lembretes, "_load_state", return_value=state):
                    with patch.object(agenda_commands.lembretes, "_events_between", return_value=[]):
                        with patch.object(agenda_commands.lembretes, "_birthdays_between", return_value=[]):
                            for command in (
                                agenda_commands.send_rotina_panel,
                                agenda_commands.send_help,
                                agenda_commands.send_status,
                                agenda_commands.send_health,
                            ):
                                with self.subTest(command=command.__name__):
                                    send_message.reset_mock()
                                    command()
                                    self.assertIsNone(send_message.call_args.kwargs["thread_id"])

    def test_debug_commands_use_expected_topics(self):
        with patch.object(agenda_commands, "send_message", return_value={"ok": True}) as send_message:
            with patch.object(agenda_commands.lembretes, "_events_between", return_value=[]):
                agenda_commands.send_debug_agenda()
                self.assertEqual(send_message.call_args.kwargs["thread_id"], THREADS["agenda"])

            with patch.object(agenda_commands.lembretes, "_birthdays_between", return_value=[]):
                agenda_commands.send_debug_aniversarios()
                self.assertEqual(send_message.call_args.kwargs["thread_id"], THREADS["aniversarios"])

    def test_agenda_and_birthday_messages_use_expected_topics(self):
        with patch.object(lembretes, "send_message", return_value={"ok": True}) as send_message:
            with patch.object(lembretes, "render_daily_events", return_value="agenda"):
                lembretes.send_daily_events()
                self.assertEqual(send_message.call_args.kwargs["thread_id"], THREADS["agenda"])

            with patch.object(lembretes, "render_daily_birthdays", return_value="aniversários"):
                lembretes.send_daily_birthdays()
                self.assertEqual(send_message.call_args.kwargs["thread_id"], THREADS["aniversarios"])

    def test_routine_panels_use_expected_topics(self):
        panels = (
            (tarefas_domesticas, tarefas_domesticas.send_panel, THREADS["tarefas"]),
            (remedios, remedios.send_prep, THREADS["remedios"]),
            (academia, academia.send_academia, THREADS["academia"]),
        )

        for module, sender, expected_thread in panels:
            with self.subTest(module=module.__name__):
                with patch.object(module, "send_message", return_value={"ok": True}) as send_message:
                    sender({})
                    self.assertEqual(send_message.call_args.kwargs["thread_id"], expected_thread)


if __name__ == "__main__":
    unittest.main()
