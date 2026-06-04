import unittest
from unittest.mock import patch

from app import main


class MainTest(unittest.TestCase):
    def test_run_calls_daily_reminders_without_import_error(self):
        expected = {"ok": True, "sent": 0}
        with patch.object(main.lembretes, "send_due_reminders", return_value=expected) as send_due_reminders:
            result = main.run()

        self.assertEqual(result, expected)
        send_due_reminders.assert_called_once()


if __name__ == "__main__":
    unittest.main()
