import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.config import GROUP_ID
from app.constants import THREADS
from app.modules.lembretes import (
    _events_between, _load_state, _save_json, _now,
    STATE_PATH,
)
from app.telegram_api import send_message

TZ = ZoneInfo("America/Sao_Paulo")

DEFAULT_REMINDERS = ["1h", "1d"]
REMINDER_WINDOWS = {
    "5m": timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "30m": timedelta(minutes=30),
    "1h": timedelta(hours=1),
    "2h": timedelta(hours=2),
    "1d": timedelta(days=1),
    "2d": timedelta(days=2),
}

LOOKAHEAD_DAYS = int(os.getenv("TOTODILE_EVENT_REMINDER_LOOKAHEAD", "7"))


def _parse_reminder_windows():
    raw = os.getenv("TOTODILE_EVENT_REMINDERS", "").strip()
    if not raw:
        return DEFAULT_REMINDERS
    windows = [w.strip() for w in raw.split(",") if w.strip() in REMINDER_WINDOWS]
    return windows if windows else DEFAULT_REMINDERS


def _reminder_key(event_id, window):
    return f"event_reminder:{event_id}:{window}"


def _already_reminded(state, key):
    sent = state.get("sent", {})
    return key in sent


def _mark_reminded(state, key, reference):
    state.setdefault("sent", {})[key] = reference.isoformat()


def _build_reminder_text(event, window_label):
    title = event["title"]
    start = event["date"]
    calendar = f" [{event['calendar']}]" if event.get("calendar") else ""
    window_desc = {
        "5m": "5 minutos",
        "15m": "15 minutos",
        "30m": "30 minutos",
        "1h": "1 hora",
        "2h": "2 horas",
        "1d": "1 dia",
        "2d": "2 dias",
    }.get(window_label, window_label)

    lines = [
        f"⏰ lembrete: {title}",
        "",
        f"{'📅' if event.get('all_day') else '🕐'} {start:%d/%m/%Y %H:%M}",
        f"⏳ daqui a {window_desc}",
    ]
    return "\n".join(lines)


def _parse_reminder_config(event):
    raw = event.get("lembretes")
    if isinstance(raw, list):
        return [w for w in raw if w in REMINDER_WINDOWS]
    if isinstance(raw, str):
        return [w.strip() for w in raw.split(",") if w.strip() in REMINDER_WINDOWS]
    return None


def send_event_reminders(reference=None):
    reference = reference or _now()
    state = _load_state()

    windows = _parse_reminder_windows()
    if not windows:
        return {"ok": True, "reminders": 0, "reason": "no_windows_configured"}

    events = _events_between(reference, LOOKAHEAD_DAYS)
    sent_count = 0

    for event in events:
        if event.get("all_day"):
            continue

        event_reminders = _parse_reminder_config(event) or windows
        if not event_reminders:
            continue

        event_id = event.get("id")
        event_start = event.get("date")

        for window in event_reminders:
            delta = REMINDER_WINDOWS.get(window)
            if delta is None:
                continue

            reminder_time = event_start - delta
            key = _reminder_key(event_id, window)

            if reference >= reminder_time and not _already_reminded(state, key):
                text = _build_reminder_text(event, window)
                send_message(GROUP_ID, text, thread_id=THREADS["agenda"])
                _mark_reminded(state, key, reference)
                sent_count += 1

    if sent_count:
        _save_json(STATE_PATH, state, "🤖 registrar lembretes de eventos")

    return {"ok": True, "reminders": sent_count}
