import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import storage


class StorageTest(unittest.TestCase):
    def test_local_load_and_save_without_github_token(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {}, clear=True), patch.object(storage, "BASE_DIR", Path(tmpdir)):
                result = storage.save_json("data/state.json", {"ok": True}, "test")
                self.assertTrue(result["ok"])
                self.assertTrue(result["local"])
                self.assertEqual(storage.load_json("data/state.json", {}), {"ok": True})

    def test_github_token_uses_github_storage(self):
        with patch.dict(os.environ, {"GITHUB_TOKEN": "token"}):
            with patch("app.storage.read_json", return_value={"remote": True}) as read_json:
                self.assertEqual(storage.load_json("data/state.json", {}), {"remote": True})
                read_json.assert_called_once_with("data/state.json", "token")

            with patch("app.storage.write_json", return_value={"ok": True}) as write_json:
                result = storage.save_json("data/state.json", {"remote": True}, "message")
                self.assertEqual(result, {"ok": True})
                write_json.assert_called_once_with(
                    "data/state.json",
                    {"remote": True},
                    "token",
                    message="message",
                )

    def test_github_missing_file_returns_fallback(self):
        with patch.dict(os.environ, {"GITHUB_TOKEN": "token"}):
            with patch("app.storage.read_json", return_value=None):
                self.assertEqual(storage.load_json("data/missing.json", {"fallback": True}), {"fallback": True})


if __name__ == "__main__":
    unittest.main()
