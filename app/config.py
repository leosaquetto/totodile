import os

BOT_TOKEN = os.getenv("TOKEN_TOTODILE")
GROUP_ID = os.getenv("ID_CENTRAL_TOTODILE")

GITHUB_REPO = "leosaquetto/totodile"
BRANCH = "main"

_ALLOWED_RAW = os.getenv("TOTODILE_ALLOWED_CHATS", "").strip()
if _ALLOWED_RAW:
    ALLOWED_CHATS = {int(c.strip()) for c in _ALLOWED_RAW.split(",") if c.strip()}
else:
    ALLOWED_CHATS = set()
