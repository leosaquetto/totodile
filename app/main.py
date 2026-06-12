import json
import logging
import time

from app.modules import lembretes
from app.config import BOT_TOKEN, GROUP_ID

LOGGER = logging.getLogger(__name__)


def validate_runtime_config():
    return {
        "has_token": bool(BOT_TOKEN),
        "has_group_id": bool(GROUP_ID),
    }


def run():
    started_at = time.perf_counter()
    cfg = validate_runtime_config()
    print(f"[totodile] config has_token={cfg['has_token']} has_group_id={cfg['has_group_id']}")
    result = lembretes.send_due_reminders()
    LOGGER.info(
        "daily_bot result=%s duration_ms=%s",
        json.dumps(result, ensure_ascii=False, sort_keys=True),
        int((time.perf_counter() - started_at) * 1000),
    )
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
