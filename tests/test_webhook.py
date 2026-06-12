import io
import json
import os
import unittest
from email.message import Message
from unittest.mock import patch

from api.telegram_webhook import handler


class WebhookTest(unittest.TestCase):
    def _request(self, method="POST", body=b"{}", headers=None):
        request = handler.__new__(handler)
        request.command = method
        request.rfile = io.BytesIO(body)
        request.wfile = io.BytesIO()
        request.headers = Message()
        request.headers["Content-Length"] = str(len(body))
        for name, value in (headers or {}).items():
            request.headers[name] = value

        statuses = []
        request.send_response = statuses.append
        request.send_header = lambda _name, _value: None
        request.end_headers = lambda: None

        getattr(request, f"do_{method}")()

        response_body = request.wfile.getvalue()
        payload = json.loads(response_body.decode("utf-8")) if response_body else None
        return statuses[0], payload

    def test_non_post_methods_return_405(self):
        with patch.dict(os.environ, {}, clear=True):
            for method in ("GET", "HEAD", "PUT", "PATCH", "DELETE", "OPTIONS", "CONNECT", "TRACE"):
                with self.subTest(method=method):
                    status, payload = self._request(method=method)
                    self.assertEqual(status, 405)
                    if method == "HEAD":
                        self.assertIsNone(payload)
                    else:
                        self.assertEqual(payload["error"], "method_not_allowed")

    def test_invalid_json_returns_400(self):
        with patch.dict(os.environ, {}, clear=True):
            status, payload = self._request(body=b"{")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "invalid_json")

    def test_non_object_payload_returns_400(self):
        with patch.dict(os.environ, {}, clear=True):
            status, payload = self._request(body=b"[]")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "payload_must_be_object")

    def test_invalid_secret_returns_403(self):
        with patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": "expected"}, clear=True):
            status, payload = self._request(
                body=b"{}",
                headers={"X-Telegram-Bot-Api-Secret-Token": "wrong"},
            )
        self.assertEqual(status, 403)
        self.assertEqual(payload["error"], "invalid_secret")

    def test_missing_secret_header_returns_403(self):
        with patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": "expected"}, clear=True):
            status, payload = self._request(body=b"{}")
        self.assertEqual(status, 403)
        self.assertEqual(payload["error"], "invalid_secret")

    def test_valid_post_calls_handle_update(self):
        with patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": "expected"}, clear=True):
            with patch("api.telegram_webhook._handle_update", return_value={"ok": True}) as handle_update:
                with self.assertLogs("api.telegram_webhook", level="INFO") as logs:
                    status, payload = self._request(
                        body=b'{"update_id": 1, "message": {"text": "/health secret text"}}',
                        headers={"X-Telegram-Bot-Api-Secret-Token": "expected"},
                    )

        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"], {"ok": True})
        handle_update.assert_called_once_with({"update_id": 1, "message": {"text": "/health secret text"}})
        self.assertIn("update_id=1", logs.output[0])
        self.assertIn("update_type=message", logs.output[0])
        self.assertIn("command=/health", logs.output[0])
        self.assertIn("duration_ms=", logs.output[0])
        self.assertNotIn("secret text", logs.output[0])

    def test_internal_error_returns_200_to_avoid_telegram_retry_loop(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("api.telegram_webhook._handle_update", side_effect=RuntimeError("boom")):
                status, payload = self._request(body=b'{"update_id": 1}')

        self.assertEqual(status, 200)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"], "internal_error")


if __name__ == "__main__":
    unittest.main()
