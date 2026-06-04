import unittest
from unittest.mock import patch

from app.hooks.main_hook import handle_update


class MainHookTest(unittest.TestCase):
    def test_non_command_message_is_ignored(self):
        result = handle_update({"message": {"text": "oi"}})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "ignored_non_command")
        self.assertEqual(result["message_type"], "message")

    def test_message_without_text_is_ignored(self):
        result = handle_update({"message": {"photo": []}})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "no_callback_or_text")

    def test_edited_message_is_routed_as_command(self):
        with patch("app.hooks.main_hook.dispatch_command", return_value={"ok": True}) as dispatch_command:
            result = handle_update({"edited_message": {"text": "/agenda"}})

        self.assertTrue(result["ok"])
        self.assertEqual(result["message_type"], "edited_message")
        dispatch_command.assert_called_once_with("/agenda")

    def test_callback_query_is_routed(self):
        callback = {"id": "cb1", "data": "agenda_hoje"}
        with patch("app.hooks.main_hook.dispatch", return_value={"ok": True}) as dispatch:
            result = handle_update({"callback_query": callback})

        self.assertTrue(result["ok"])
        dispatch.assert_called_once_with(callback)

    def test_invalid_callback_query_is_rejected(self):
        result = handle_update({"callback_query": "invalid"})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "invalid_callback_query")


if __name__ == "__main__":
    unittest.main()
