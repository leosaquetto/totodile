import json
import base64
import requests
from app.config import GITHUB_REPO, BRANCH

API = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
MAX_RESPONSE_TEXT = 1000


class GithubContentError(RuntimeError):
    def __init__(self, action, path, status, response_text):
        self.action = action
        self.path = path
        self.status = status
        self.response_text = response_text
        super().__init__(
            f"GitHub contents {action} failed: path={path} status={status} response={response_text}"
        )


def _headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Totodile-Bot",
    }


def _response_text(response):
    text = response.text or ""
    if len(text) <= MAX_RESPONSE_TEXT:
        return text
    return f"{text[:MAX_RESPONSE_TEXT]}...<truncated>"


def _content_url(path, ref=None):
    url = f"{API}/{path}"
    if ref:
        return f"{url}?ref={ref}"
    return url


def _read_metadata(path, token):
    response = requests.get(_content_url(path, ref=BRANCH), headers=_headers(token), timeout=30)
    if response.status_code == 404:
        return None
    if not response.ok:
        raise GithubContentError("read", path, response.status_code, _response_text(response))
    return response.json()


def read_json(path, token):
    data = _read_metadata(path, token)
    if data is None:
        return None

    content = base64.b64decode(data["content"]).decode("utf-8")
    return json.loads(content) if content else {}


def _encoded_content(content):
    encoded = base64.b64encode(
        json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")
    return encoded


def write_json(path, content, token, message="update json", retries=1):
    url = _content_url(path)

    for attempt in range(retries + 1):
        metadata = _read_metadata(path, token)
        sha = metadata.get("sha") if isinstance(metadata, dict) else None

        payload = {
            "message": message,
            "content": _encoded_content(content),
            "branch": BRANCH,
        }

        if sha:
            payload["sha"] = sha

        response = requests.put(url, json=payload, headers=_headers(token), timeout=30)
        if response.status_code == 409 and attempt < retries:
            continue
        if not response.ok:
            raise GithubContentError("write", path, response.status_code, _response_text(response))
        return response.json()

    raise GithubContentError("write", path, 409, "conflict after retry")
