import io
import json
import os
import unittest
from email.message import Message
from unittest.mock import patch

from api.health import handler


class HealthEndpointTest(unittest.TestCase):
    def _request(self, method="GET"):
        request = handler.__new__(handler)
        request.command = method
        request.rfile = io.BytesIO()
        request.wfile = io.BytesIO()
        request.headers = Message()

        statuses = []
        headers = {}
        request.send_response = statuses.append
        request.send_header = lambda name, value: headers.__setitem__(name, value)
        request.end_headers = lambda: None

        getattr(request, f"do_{method}")()

        response_body = request.wfile.getvalue()
        payload = json.loads(response_body.decode("utf-8")) if response_body else None
        return statuses[0], headers, payload

    def test_get_returns_public_health_payload(self):
        env = {
            "TOKEN_TOTODILE": "telegram-token",
            "ID_CENTRAL_TOTODILE": "-100",
            "GITHUB_TOKEN": "github-token",
        }
        with patch.dict(os.environ, env, clear=True):
            status, _headers, payload = self._request()

        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["service"], "totodile")
        self.assertTrue(payload["has_token"])
        self.assertTrue(payload["has_group_id"])
        self.assertTrue(payload["has_github_token"])
        self.assertNotIn("telegram-token", json.dumps(payload))
        self.assertNotIn("github-token", json.dumps(payload))

    def test_non_get_returns_405(self):
        status, headers, payload = self._request(method="POST")

        self.assertEqual(status, 405)
        self.assertEqual(headers["Allow"], "GET")
        self.assertEqual(payload["error"], "method_not_allowed")


if __name__ == "__main__":
    unittest.main()
