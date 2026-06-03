import base64
import json
import unittest
from unittest.mock import patch

from app import github_db


class FakeResponse:
    def __init__(self, status_code, payload=None, text=""):
        self.status_code = status_code
        self.payload = payload or {}
        self.text = text
        self.ok = 200 <= status_code < 300

    def json(self):
        return self.payload


class GithubDbTest(unittest.TestCase):
    def test_read_json_decodes_content(self):
        encoded = base64.b64encode(json.dumps({"ok": True}).encode("utf-8")).decode("utf-8")
        with patch("app.github_db.requests.get", return_value=FakeResponse(200, {"content": encoded})):
            self.assertEqual(github_db.read_json("data/state.json", "token"), {"ok": True})

    def test_write_json_retries_conflict_once(self):
        get_responses = [
            FakeResponse(200, {"sha": "old"}),
            FakeResponse(200, {"sha": "new"}),
        ]
        put_responses = [
            FakeResponse(409, text="conflict"),
            FakeResponse(200, {"ok": True}),
        ]

        with patch("app.github_db.requests.get", side_effect=get_responses) as get:
            with patch("app.github_db.requests.put", side_effect=put_responses) as put:
                result = github_db.write_json("data/state.json", {"ok": True}, "token", retries=1)

        self.assertEqual(result, {"ok": True})
        self.assertEqual(get.call_count, 2)
        self.assertEqual(put.call_count, 2)

    def test_write_json_raises_contextual_error(self):
        with patch("app.github_db.requests.get", return_value=FakeResponse(200, {"sha": "old"})):
            with patch("app.github_db.requests.put", return_value=FakeResponse(500, text="server error")):
                with self.assertRaises(github_db.GithubContentError) as error:
                    github_db.write_json("data/state.json", {"ok": True}, "token", retries=0)

        self.assertIn("path=data/state.json", str(error.exception))
        self.assertIn("status=500", str(error.exception))
        self.assertNotIn("token", str(error.exception))


if __name__ == "__main__":
    unittest.main()
