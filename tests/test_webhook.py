import json
import os
import threading
import unittest
from http.server import HTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

from api.telegram_webhook import handler


class WebhookTest(unittest.TestCase):
    def _request(self, method="POST", body=b"{}", headers=None):
        server = HTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.handle_request)
        thread.start()

        url = f"http://127.0.0.1:{server.server_port}/api/telegram_webhook"
        request = Request(url, data=body if method != "GET" else None, method=method, headers=headers or {})

        try:
            response = urlopen(request, timeout=5)
            status = response.status
            payload = response.read()
        except HTTPError as error:
            status = error.code
            payload = error.read()
        finally:
            thread.join(timeout=5)
            server.server_close()

        return status, json.loads(payload.decode("utf-8"))

    def test_get_returns_405(self):
        with patch.dict(os.environ, {}, clear=True):
            status, payload = self._request(method="GET")
        self.assertEqual(status, 405)
        self.assertEqual(payload["error"], "method_not_allowed")

    def test_invalid_json_returns_400(self):
        with patch.dict(os.environ, {}, clear=True):
            status, payload = self._request(body=b"{")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"], "invalid_json")

    def test_invalid_secret_returns_403(self):
        with patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": "expected"}, clear=True):
            status, payload = self._request(
                body=b"{}",
                headers={"X-Telegram-Bot-Api-Secret-Token": "wrong"},
            )
        self.assertEqual(status, 403)
        self.assertEqual(payload["error"], "invalid_secret")

    def test_valid_post_calls_handle_update(self):
        with patch.dict(os.environ, {"TELEGRAM_WEBHOOK_SECRET": "expected"}, clear=True):
            with patch("api.telegram_webhook._handle_update", return_value={"ok": True}) as handle_update:
                status, payload = self._request(
                    body=b'{"update_id": 1}',
                    headers={"X-Telegram-Bot-Api-Secret-Token": "expected"},
                )

        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["result"], {"ok": True})
        handle_update.assert_called_once_with({"update_id": 1})

    def test_internal_error_returns_200_to_avoid_telegram_retry_loop(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("api.telegram_webhook._handle_update", side_effect=RuntimeError("boom")):
                status, payload = self._request(body=b'{"update_id": 1}')

        self.assertEqual(status, 200)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"], "internal_error")


if __name__ == "__main__":
    unittest.main()
