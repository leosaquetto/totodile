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
            update = {"edited_message": {"text": "/agenda"}}
            result = handle_update(update)

        self.assertTrue(result["ok"])
        self.assertEqual(result["message_type"], "edited_message")
        dispatch_command.assert_called_once_with("/agenda", message=update["edited_message"])

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

    def test_unauthorized_message_is_rejected_when_allowlist_active(self):
        with patch("app.hooks.main_hook.ALLOWED_CHATS", {-1001234567890}):
            result = handle_update({
                "message": {
                    "text": "/agenda",
                    "chat": {"id": -999999999999},
                }
            })

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "unauthorized_chat")

    def test_authorized_message_is_accepted_when_allowlist_active(self):
        allowed_id = -1001234567890
        with patch("app.hooks.main_hook.ALLOWED_CHATS", {allowed_id}):
            with patch("app.hooks.main_hook.dispatch_command", return_value={"ok": True}) as dc:
                update = {
                    "message": {
                        "text": "/agenda",
                        "chat": {"id": allowed_id},
                    }
                }
                result = handle_update(update)

        self.assertTrue(result["ok"])
        dc.assert_called_once()

    def test_unauthorized_callback_is_rejected_when_allowlist_active(self):
        with patch("app.hooks.main_hook.ALLOWED_CHATS", {-1001234567890}):
            result = handle_update({
                "callback_query": {
                    "id": "cb1",
                    "data": "agenda_hoje",
                    "message": {
                        "chat": {"id": -999999999999},
                        "message_id": 10,
                    }
                }
            })

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "unauthorized_chat")

    def test_message_without_chat_id_is_rejected_when_allowlist_active(self):
        with patch("app.hooks.main_hook.ALLOWED_CHATS", {-1001234567890}):
            result = handle_update({"message": {"text": "/agenda"}})

        self.assertFalse(result["ok"])
        self.assertEqual(result["reason"], "unauthorized_chat")

    def test_empty_allowlist_allows_all(self):
        with patch("app.hooks.main_hook.ALLOWED_CHATS", set()):
            with patch("app.hooks.main_hook.dispatch_command", return_value={"ok": True}):
                result = handle_update({
                    "message": {
                        "text": "/agenda",
                        "chat": {"id": -999999999999},
                    }
                })

        self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
