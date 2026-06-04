import hmac
import json
import logging
import os
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

LOGGER = logging.getLogger(__name__)
MAX_BODY_BYTES = 1024 * 1024


def _json_bytes(payload):
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def _handle_update(update):
    from app.hooks.main_hook import handle_update

    return handle_update(update)


class handler(BaseHTTPRequestHandler):
    server_version = "TotodileTelegramWebhook/1.0"

    def do_POST(self):
        secret_error = self._validate_secret()
        if secret_error:
            self._send_json(*secret_error)
            return

        try:
            payload = self._read_json_body()
        except ValueError:
            self._send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "invalid_json"})
            return

        if not isinstance(payload, dict):
            self._send_json(HTTPStatus.BAD_REQUEST, {"ok": False, "error": "payload_must_be_object"})
            return

        try:
            result = _handle_update(payload)
        except Exception:
            LOGGER.exception("telegram_webhook internal_error update_id=%s", payload.get("update_id"))
            self._send_json(HTTPStatus.OK, {"ok": False, "error": "internal_error"})
            return

        self._send_json(HTTPStatus.OK, {"ok": True, "result": result})

    def do_GET(self):
        self._method_not_allowed()

    def do_HEAD(self):
        self._method_not_allowed()

    def do_PUT(self):
        self._method_not_allowed()

    def do_PATCH(self):
        self._method_not_allowed()

    def do_DELETE(self):
        self._method_not_allowed()

    def do_OPTIONS(self):
        self._method_not_allowed()

    def do_CONNECT(self):
        self._method_not_allowed()

    def do_TRACE(self):
        self._method_not_allowed()

    def _validate_secret(self):
        expected_secret = os.getenv("TELEGRAM_WEBHOOK_SECRET")
        if not expected_secret:
            return None

        received_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if not received_secret or not hmac.compare_digest(received_secret, expected_secret):
            return HTTPStatus.FORBIDDEN, {"ok": False, "error": "invalid_secret"}
        return None

    def _read_json_body(self):
        raw_length = self.headers.get("Content-Length") or "0"
        try:
            content_length = int(raw_length)
        except ValueError as exc:
            raise ValueError("invalid content length") from exc

        if content_length < 1 or content_length > MAX_BODY_BYTES:
            raise ValueError("invalid body size")

        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("invalid json") from exc

    def _method_not_allowed(self):
        self._send_json(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {"ok": False, "error": "method_not_allowed"},
            extra_headers={"Allow": "POST"},
        )

    def _send_json(self, status, payload, extra_headers=None):
        body = _json_bytes(payload)
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
