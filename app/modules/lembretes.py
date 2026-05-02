import json
import os
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.config import GROUP_ID
from app.constants import THREADS
from app.github_db import read_json, write_json
from app.telegram_api import send_message

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BIRTHDAYS_PATH = "data/aniversarios/aniversarios.json"
EVENTS_PATH = "data/agenda/eventos.json"
STATE_PATH = "data/lembretes/sent_state.json"
TOKEN = os.getenv("GITHUB_TOKEN")

BIRTHDAY_CALENDARS = {"aniversários", "birthdays"}
EVENT_LOOKAHEAD_HOURS = int(os.getenv("TOTODILE_EVENT_LOOKAHEAD_HOURS", "24"))
BIRTHDAY_LOOKAHEAD_DAYS = int(os.getenv("TOTODILE_BIRTHDAY_LOOKAHEAD_DAYS", "1"))


def _now():
    return datetime.now().astimezone()


def _load_local_json(path, fallback):
    full_path = BASE_DIR / path
    if not full_path.exists():
        return fallback
    try:
        return json.loads(full_path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def _load_json(path, fallback):
    if TOKEN:
        data = read_json(path, TOKEN)
        if data is not None:
            return data
    return _load_local_json(path, fallback)


def _save_json(path, data, message):
    if TOKEN:
        return write_json(path, data, TOKEN, message=message)

    full_path = BASE_DIR / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "local": True}


def _items(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("items", "events", "aniversarios", "birthdays", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return value
        return [dict(value, id=key) for key, value in data.items() if isinstance(value, dict)]
    return []


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value / 1000 if value > 10_000_000_000 else value).astimezone()
        except Exception:
            return None

    text = str(value).strip()
    if not text:
        return None

    iso = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(iso).astimezone()
    except Exception:
        pass

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y"):
        try:
            return datetime.strptime(text[:10], fmt).replace(tzinfo=_now().tzinfo)
        except Exception:
            continue
    return None


def _slug(text):
    normalized = unicodedata.normalize("NFD", str(text or ""))
    clean = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return "".join(ch.lower() for ch in clean if ch.isalnum()) or "item"


def _clean_birthday_name(title):
    name = str(title or "").strip()
    for prefix in ("Aniversário de ", "Aniversário do ", "Aniversário da ", "Birthday of "):
        if name.lower().startswith(prefix.lower()):
            name = name[len(prefix):]
            break
    return name.strip() or "Aniversário"


def _day_label(days):
    if days == 0:
        return "HOJE"
    if days == 1:
        return "AMANHÃ"
    return f"EM {days} DIAS"


def _date_line(dt, include_year=True):
    weekday = dt.strftime("%A")
    weekdays = {
        "Monday": "segunda-feira",
        "Tuesday": "terça-feira",
        "Wednesday": "quarta-feira",
        "Thursday": "quinta-feira",
        "Friday": "sexta-feira",
        "Saturday": "sábado",
        "Sunday": "domingo",
    }
    weekday = weekdays.get(weekday, weekday)
    if include_year:
        return f"{dt:%d/%m/%y}, {weekday}"
    return f"{dt:%d/%m}, {weekday}"


def _time_line(dt, is_all_day=False):
    if is_all_day:
        return _date_line(dt, include_year=True)
    return f"{_date_line(dt, include_year=True)} - {dt:%H:%M}"


def _next_birthday_dt(dt, reference):
    candidate = dt.replace(year=reference.year, hour=0, minute=0, second=0, microsecond=0)
    if candidate.date() < reference.date():
        candidate = candidate.replace(year=reference.year + 1)
    return candidate


def _birthdays_due(reference):
    data = _load_json(BIRTHDAYS_PATH, [])
    due = []
    today = reference.date()

    for raw in _items(data):
        title = raw.get("nome") or raw.get("name") or raw.get("title") or raw.get("titulo")
        date_value = raw.get("data") or raw.get("date") or raw.get("birthday") or raw.get("startDate")
        original_dt = _parse_date(date_value)
        if not title or not original_dt:
            continue

        next_dt = _next_birthday_dt(original_dt, reference)
        days = (next_dt.date() - today).days
        if 0 <= days <= BIRTHDAY_LOOKAHEAD_DAYS:
            age = raw.get("idade") or raw.get("age")
            if not age and original_dt.year < next_dt.year:
                age = next_dt.year - original_dt.year
            due.append({
                "id": raw.get("id") or _slug(title),
                "title": _clean_birthday_name(title),
                "date": next_dt,
                "days": days,
                "age": age,
            })

    due.sort(key=lambda item: item["date"])
    return due


def _events_due(reference):
    data = _load_json(EVENTS_PATH, [])
    due = []
    end = reference + timedelta(hours=EVENT_LOOKAHEAD_HOURS)

    for raw in _items(data):
        title = raw.get("title") or raw.get("titulo") or raw.get("name") or raw.get("nome")
        start_value = raw.get("startDate") or raw.get("start") or raw.get("data") or raw.get("date")
        start_dt = _parse_date(start_value)
        end_dt = _parse_date(raw.get("endDate") or raw.get("end"))
        if not title or not start_dt:
            continue

        calendar = raw.get("calendar") or raw.get("calendario") or ""
        if isinstance(calendar, dict):
            calendar = calendar.get("title") or calendar.get("name") or ""
        if str(calendar).strip().lower() in BIRTHDAY_CALENDARS:
            continue

        if end_dt and end_dt < reference:
            continue
        if reference <= start_dt <= end:
            days = (start_dt.date() - reference.date()).days
            due.append({
                "id": raw.get("id") or f"{_slug(title)}-{start_dt.isoformat()}",
                "title": str(title).strip(),
                "date": start_dt,
                "days": days,
                "all_day": bool(raw.get("isAllDay") or raw.get("allDay") or raw.get("diaInteiro")),
                "calendar": str(calendar).strip(),
            })

    due.sort(key=lambda item: item["date"])
    return due


def _load_state():
    state = _load_json(STATE_PATH, {"sent": {}})
    if not isinstance(state, dict):
        state = {"sent": {}}
    state.setdefault("sent", {})
    return state


def _already_sent(state, key):
    return bool(state.get("sent", {}).get(key))


def _mark_sent(state, key, reference):
    state.setdefault("sent", {})[key] = reference.isoformat()


def _prune_state(state, reference):
    cutoff = reference - timedelta(days=14)
    sent = state.get("sent", {})
    kept = {}
    for key, value in sent.items():
        dt = _parse_date(value)
        if dt and dt >= cutoff:
            kept[key] = value
    state["sent"] = kept


def _send_birthday(item):
    age_line = f"\nidade: {item['age']} anos" if item.get("age") else ""
    text = (
        f"🎈 aniversário {_day_label(item['days']).lower()}\n\n"
        f"{item['title']}\n"
        f"{_date_line(item['date'])}"
        f"{age_line}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["aniversarios"])


def _send_event(item):
    calendar_line = f"\ncalendário: {item['calendar']}" if item.get("calendar") else ""
    text = (
        f"🗓️ compromisso {_day_label(item['days']).lower()}\n\n"
        f"{item['title']}\n"
        f"{_time_line(item['date'], item.get('all_day'))}"
        f"{calendar_line}"
    )
    return send_message(GROUP_ID, text, thread_id=THREADS["agenda"])


def send_due_reminders():
    reference = _now()
    state = _load_state()
    _prune_state(state, reference)

    sent_count = 0

    for item in _birthdays_due(reference):
        key = f"birthday:{item['id']}:{item['date'].date().isoformat()}:{item['days']}"
        if _already_sent(state, key):
            continue
        _send_birthday(item)
        _mark_sent(state, key, reference)
        sent_count += 1

    for item in _events_due(reference):
        key = f"event:{item['id']}:{item['date'].isoformat()}"
        if _already_sent(state, key):
            continue
        _send_event(item)
        _mark_sent(state, key, reference)
        sent_count += 1

    if sent_count:
        _save_json(STATE_PATH, state, "🤖 registrar lembretes enviados")

    return {"ok": True, "sent": sent_count}
