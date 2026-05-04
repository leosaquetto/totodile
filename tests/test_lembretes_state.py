import unittest

from app.modules import lembretes


class LembretesStateTest(unittest.TestCase):
    def test_load_state_defaults(self):
        state = lembretes._load_state()
        self.assertIn("sent", state)
        self.assertIn("read", state)
        self.assertIn("snoozed", state)
        self.assertIn("last_daily_summary", state)


if __name__ == "__main__":
    unittest.main()
