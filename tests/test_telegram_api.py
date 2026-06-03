import json
import unittest
from unittest.mock import patch

import requests

from app import telegram_api


class FakeResponse:
    ok = True
    status_code = 200
    text = '{"ok": true}'

    def json(self):
        return {"ok": True}


class TelegramApiTest(unittest.TestCase):
    def test_send_message_omits_empty_thread_id(self):
        with patch.object(telegram_api, "BOT_TOKEN", "secret-token"):
            with patch("app.telegram_api.requests.post", return_value=FakeResponse()) as post:
                telegram_api.send_message(123, "oi", thread_id=None)

        payload = post.call_args.kwargs["json"]
        self.assertNotIn("message_thread_id", payload)

    def test_send_message_serializes_reply_markup(self):
        reply_markup = {"inline_keyboard": [[{"text": "ok", "callback_data": "ok"}]]}
        with patch.object(telegram_api, "BOT_TOKEN", "secret-token"):
            with patch("app.telegram_api.requests.post", return_value=FakeResponse()) as post:
                telegram_api.send_message(123, "oi", reply_markup=reply_markup)

        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["reply_markup"], json.dumps(reply_markup, ensure_ascii=False))

    def test_send_message_does_not_set_parse_mode_by_default(self):
        with patch.object(telegram_api, "BOT_TOKEN", "secret-token"):
            with patch("app.telegram_api.requests.post", return_value=FakeResponse()) as post:
                telegram_api.send_message(123, "<texto>")

        payload = post.call_args.kwargs["json"]
        self.assertNotIn("parse_mode", payload)

    def test_request_error_does_not_log_token(self):
        with patch.object(telegram_api, "BOT_TOKEN", "secret-token"):
            with patch("app.telegram_api.requests.post", side_effect=requests.RequestException("boom")):
                with self.assertRaises(RuntimeError) as error:
                    telegram_api.send_message(123, "oi")

        self.assertNotIn("secret-token", str(error.exception))

    def test_missing_chat_id_fails_before_request(self):
        with patch.object(telegram_api, "BOT_TOKEN", "secret-token"):
            with patch("app.telegram_api.requests.post") as post:
                with self.assertRaises(RuntimeError):
                    telegram_api.send_message(None, "oi")

        post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
