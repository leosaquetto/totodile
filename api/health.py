import json
import os
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler


def _json_bytes(payload):
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def _health_payload():
    return {
        "ok": True,
        "service": "totodile",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "has_token": bool(os.getenv("TOKEN_TOTODILE")),
        "has_group_id": bool(os.getenv("ID_CENTRAL_TOTODILE")),
        "has_github_token": bool(os.getenv("GITHUB_TOKEN")),
    }


class handler(BaseHTTPRequestHandler):
    server_version = "TotodileHealth/1.0"

    def do_GET(self):
        self._send_json(HTTPStatus.OK, _health_payload())

    def do_POST(self):
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

    def _method_not_allowed(self):
        self._send_json(
            HTTPStatus.METHOD_NOT_ALLOWED,
            {"ok": False, "error": "method_not_allowed"},
            extra_headers={"Allow": "GET"},
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
