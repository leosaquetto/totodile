import json
import logging
import time

from app.modules.event_reminders import send_event_reminders

LOGGER = logging.getLogger(__name__)


def run():
    started_at = time.perf_counter()
    result = send_event_reminders()
    LOGGER.info(
        "event_reminders result=%s duration_ms=%s",
        json.dumps(result, ensure_ascii=False, sort_keys=True),
        int((time.perf_counter() - started_at) * 1000),
    )
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
