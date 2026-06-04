import json
import unittest
from unittest.mock import patch

from scripts import delete_telegram_webhook, get_telegram_webhook_info, set_telegram_webhook


class FakeResponse:
    def __init__(self, payload=None):
        self.payload = [] if payload is None else payload
        self.text = json.dumps(self.payload)

    def json(self):
        return self.payload


class WebhookScriptsTest(unittest.TestCase):
    def test_set_webhook_payload_with_secret(self):
        env = {
            "TOKEN_TOTODILE": "token",
            "TELEGRAM_WEBHOOK_URL": "https://example.test/webhook",
            "TELEGRAM_WEBHOOK_SECRET": "secret",
        }
        with patch.dict("os.environ", env, clear=True):
            with patch.object(
                set_telegram_webhook.requests,
                "post",
                return_value=FakeResponse({"ok": True}),
            ) as post:
                self.assertEqual(set_telegram_webhook.main(), 0)

        self.assertEqual(
            post.call_args.kwargs["json"],
            {
                "url": "https://example.test/webhook",
                "allowed_updates": ["message", "edited_message", "callback_query"],
                "drop_pending_updates": False,
                "secret_token": "secret",
            },
        )

    def test_set_webhook_omits_empty_secret(self):
        env = {"TOKEN_TOTODILE": "token", "TELEGRAM_WEBHOOK_URL": "https://example.test/webhook"}
        with patch.dict("os.environ", env, clear=True):
            with patch.object(
                set_telegram_webhook.requests,
                "post",
                return_value=FakeResponse({"ok": True}),
            ) as post:
                self.assertEqual(set_telegram_webhook.main(), 0)

        self.assertNotIn("secret_token", post.call_args.kwargs["json"])

    def test_set_webhook_non_object_json_returns_nonzero(self):
        env = {"TOKEN_TOTODILE": "token", "TELEGRAM_WEBHOOK_URL": "https://example.test/webhook"}
        with patch.dict("os.environ", env, clear=True):
            with patch.object(set_telegram_webhook.requests, "post", return_value=FakeResponse()):
                self.assertEqual(set_telegram_webhook.main(), 1)

    def test_get_webhook_info_non_object_json_returns_nonzero(self):
        with patch.dict("os.environ", {"TOKEN_TOTODILE": "token"}, clear=True):
            with patch.object(get_telegram_webhook_info.requests, "get", return_value=FakeResponse()):
                self.assertEqual(get_telegram_webhook_info.main(), 1)

    def test_delete_webhook_non_object_json_returns_nonzero(self):
        with patch.dict("os.environ", {"TOKEN_TOTODILE": "token"}, clear=True):
            with patch("sys.argv", ["delete_telegram_webhook.py"]):
                with patch.object(delete_telegram_webhook.requests, "post", return_value=FakeResponse()):
                    self.assertEqual(delete_telegram_webhook.main(), 1)

    def test_delete_webhook_keeps_pending_updates_by_default(self):
        with patch.dict("os.environ", {"TOKEN_TOTODILE": "token"}, clear=True):
            with patch("sys.argv", ["delete_telegram_webhook.py"]):
                with patch.object(
                    delete_telegram_webhook.requests,
                    "post",
                    return_value=FakeResponse({"ok": True}),
                ) as post:
                    self.assertEqual(delete_telegram_webhook.main(), 0)

        self.assertEqual(post.call_args.kwargs["json"], {"drop_pending_updates": False})


if __name__ == "__main__":
    unittest.main()
