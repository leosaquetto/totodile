import json
import logging
import time

from app.modules import lembretes

LOGGER = logging.getLogger(__name__)


def run():
    started_at = time.perf_counter()
    result = lembretes.send_snoozed_agenda_reminders()
    LOGGER.info(
        "snooze_bot result=%s duration_ms=%s",
        json.dumps(result, ensure_ascii=False, sort_keys=True),
        int((time.perf_counter() - started_at) * 1000),
    )
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
