import json
import base64
import requests
from app.config import GITHUB_REPO, BRANCH

API = f"https://api.github.com/repos/{GITHUB_REPO}/contents"


def read_json(path, token):
    url = f"{API}/{path}?ref={BRANCH}"
    headers = {"Authorization": f"token {token}"}

    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code != 200:
        return None

    data = r.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return json.loads(content) if content else {}


def write_json(path, content, token, message="update json"):
    url = f"{API}/{path}"
    headers = {"Authorization": f"token {token}"}

    r = requests.get(url, headers=headers, timeout=30)
    sha = r.json()["sha"] if r.status_code == 200 else None

    encoded = base64.b64encode(
        json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")

    payload = {
        "message": message,
        "content": encoded,
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha

    resp = requests.put(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()
