import unittest
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from app.modules import lembretes


class LembretesStateTest(unittest.TestCase):
    def test_load_state_defaults(self):
        with patch.dict("os.environ", {}, clear=True):
            state = lembretes._load_state()
        self.assertIn("sent", state)
        self.assertIn("read", state)
        self.assertIn("snoozed", state)
        self.assertIn("last_daily_summary", state)

    def test_date_only_value_is_interpreted_in_bot_timezone(self):
        parsed = lembretes._parse_date("2026-06-04")

        self.assertEqual(parsed.isoformat(), "2026-06-04T00:00:00-03:00")

    def test_leap_day_birthday_does_not_crash_in_non_leap_year(self):
        birthday = datetime(2024, 2, 29, tzinfo=ZoneInfo("America/Sao_Paulo"))
        reference = datetime(2026, 1, 1, tzinfo=ZoneInfo("America/Sao_Paulo"))

        result = lembretes._next_birthday_dt(birthday, reference)

        self.assertEqual(result.date().isoformat(), "2026-02-28")

    def test_snoozed_agenda_without_events_is_not_marked_as_sent(self):
        reference = datetime(2026, 6, 4, 12, tzinfo=ZoneInfo("America/Sao_Paulo"))
        state = {
            "sent": {},
            "read": {},
            "snoozed": {"snooze_agenda:2026-06-04": {"requested_at": reference.isoformat()}},
            "last_daily_summary": None,
        }

        with patch.object(lembretes, "_load_state", return_value=state):
            with patch.object(lembretes, "send_daily_events", return_value=None):
                with patch.object(lembretes, "_save_json") as save_json:
                    result = lembretes.send_snoozed_agenda_reminders(reference)

        self.assertEqual(result, {"ok": True, "sent": 0, "reason": "no_events_for_today"})
        self.assertNotIn("snooze_sent_agenda:2026-06-04", state["sent"])
        save_json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
