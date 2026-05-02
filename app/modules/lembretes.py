import json
import os
import unicodedata
from datetime import datetime, timedelta
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
BIRTHDAY_LOOKAHEAD_DAYS = int(os.getenv("TOTODILE_BIRTHDAY_LOOKAHEAD_DAYS", "1"))
WEEK_LOOKAHEAD_DAYS = int(os.getenv("TOTODILE_WEEK_LOOKAHEAD_DAYS", "7"))


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
        return "dia inteiro"
    return f"{dt:%H:%M}"


def _next_birthday_dt(dt, reference):
    candidate = dt.replace(year=reference.year, hour=0, minute=0, second=0, microsecond=0)
    if candidate.date() < reference.date():
        candidate = candidate.replace(year=reference.year + 1)
    return candidate


def _birthday_item(raw, reference):
    title = raw.get("nome") or raw.get("name") or raw.get("title") or raw.get("titulo")
    date_value = raw.get("data") or raw.get("date") or raw.get("birthday") or raw.get("startDate")
    original_dt = _parse_date(date_value)
    if not title or not original_dt:
        return None

    next_dt = _next_birthday_dt(original_dt, reference)
    days = (next_dt.date() - reference.date()).days
    age = raw.get("idade") or raw.get("age")
    if not age and original_dt.year < next_dt.year:
        age = next_dt.year - original_dt.year

    return {
        "id": raw.get("id") or raw.get("fileName") or _slug(title),
        "title": _clean_birthday_name(title),
        "date": next_dt,
        "days": days,
        "age": age,
        "file_name": raw.get("fileName"),
        "widget_name": raw.get("nomeWidget"),
        "date_line": raw.get("dateLine") or _date_line(next_dt),
    }


def _event_item(raw):
    title = raw.get("title") or raw.get("titulo") or raw.get("name") or raw.get("nome")
    start_value = raw.get("startDate") or raw.get("start") or raw.get("data") or raw.get("date")
    start_dt = _parse_date(start_value)
    end_dt = _parse_date(raw.get("endDate") or raw.get("end"))
    if not title or not start_dt:
        return None

    calendar = raw.get("calendar") or raw.get("calendario") or ""
    if isinstance(calendar, dict):
        calendar = calendar.get("title") or calendar.get("name") or ""
    if str(calendar).strip().lower() in BIRTHDAY_CALENDARS:
        return None

    return {
        "id": raw.get("id") or f"{_slug(title)}-{start_dt.isoformat()}",
        "title": str(title).strip(),
        "date": start_dt,
        "end_date": end_dt,
        "all_day": bool(raw.get("isAllDay") or raw.get("allDay") or raw.get("diaInteiro")),
        "calendar": str(calendar).strip(),
        "date_line": raw.get("dateLine") or _date_line(start_dt),
    }


def _birthdays_between(reference, days_ahead):
    data = _load_json(BIRTHDAYS_PATH, [])
    end_date = reference.date() + timedelta(days=days_ahead)
    birthdays = []

    for raw in _items(data):
        item = _birthday_item(raw, reference)
        if not item:
            continue
        if reference.date() <= item["date"].date() <= end_date:
            birthdays.append(item)

    birthdays.sort(key=lambda item: item["date"])
    return birthdays


def _events_between(reference, days_ahead):
    data = _load_json(EVENTS_PATH, [])
    end_date = reference.date() + timedelta(days=days_ahead)
    events = []

    for raw in _items(data):
        item = _event_item(raw)
        if not item:
            continue
        if item["end_date"] and item["end_date"].date() < reference.date():
            continue
        if reference.date() <= item["date"].date() <= end_date:
            item["days"] = (item["date"].date() - reference.date()).days
            events.append(item)

    events.sort(key=lambda item: item["date"])
    return events


def _birthdays_today(reference):
    return [item for item in _birthdays_between(reference, BIRTHDAY_LOOKAHEAD_DAYS) if item["date"].date() == reference.date()]


def _events_today(reference):
    return [item for item in _events_between(reference, 0) if item["date"].date() == reference.date()]


def _load_state():
    state = _load_json(STATE_PATH, {"sent": {}})
    if not isinstance(state, dict):
        state = {"sent": {}}

    state.setdefault("sent", {})
    state.setdefault("read", {})
    state.setdefault("snoozed", {})
    state.setdefault("last_daily_summary", None)

    if not isinstance(state.get("sent"), dict):
        state["sent"] = {}
    if not isinstance(state.get("read"), dict):
        state["read"] = {}
    if not isinstance(state.get("snoozed"), dict):
        state["snoozed"] = {}

    return state


def _already_sent(state, key):
    return bool(state.get("sent", {}).get(key))


def _mark_sent(state, key, reference):
    state.setdefault("sent", {})[key] = reference.isoformat()


def _prune_state(state, reference):
    sent_cutoff = reference - timedelta(days=14)
    aux_cutoff = reference - timedelta(days=30)

    sent = state.get("sent", {})
    kept_sent = {}
    for key, value in sent.items():
        dt = _parse_date(value)
        if dt and dt >= sent_cutoff:
            kept_sent[key] = value
    state["sent"] = kept_sent

    read = state.get("read", {})
    kept_read = {}
    for key, value in read.items():
        dt = _parse_date(value)
        if dt and dt >= aux_cutoff:
            kept_read[key] = value
    state["read"] = kept_read

    snoozed = state.get("snoozed", {})
    kept_snoozed = {}
    for key, value in snoozed.items():
        if isinstance(value, dict):
            dt = _parse_date(value.get("requested_at") or value.get("at"))
        else:
            dt = _parse_date(value)
        if dt and dt >= aux_cutoff:
            kept_snoozed[key] = value
    state["snoozed"] = kept_snoozed


def _birthday_line(item):
    age = f" — {item['age']} anos" if item.get("age") else ""
    return f"• {item['title']}{age}"


def _event_line(item):
    calendar = f" · {item['calendar']}" if item.get("calendar") else ""
    return f"• {_time_line(item['date'], item.get('all_day'))} — {item['title']}{calendar}"


def render_daily_birthdays(reference=None):
    reference = reference or _now()
    birthdays = _birthdays_today(reference)
    if not birthdays:
        return None
    lines = ["🎈 aniversários de hoje", "", *[_birthday_line(item) for item in birthdays]]
    return "\n".join(lines)


def render_daily_events(reference=None):
    reference = reference or _now()
    events = _events_today(reference)
    if not events:
        return None
    lines = ["🗓️ agenda de hoje", "", *[_event_line(item) for item in events]]
    return "\n".join(lines)


def render_week_birthdays(reference=None):
    reference = reference or _now()
    birthdays = _birthdays_between(reference, WEEK_LOOKAHEAD_DAYS)
    if not birthdays:
        return "🎈 aniversários da semana\n\nnenhum aniversário nos próximos dias."
    lines = ["🎈 aniversários da semana", ""]
    for item in birthdays:
        lines.append(f"• {_date_line(item['date'], include_year=False)} — {item['title']}" + (f" ({item['age']} anos)" if item.get("age") else ""))
    return "\n".join(lines)


def render_week_events(reference=None):
    reference = reference or _now()
    events = _events_between(reference, WEEK_LOOKAHEAD_DAYS)
    if not events:
        return "🗓️ eventos da semana\n\nnenhum compromisso nos próximos dias."
    lines = ["🗓️ eventos da semana", ""]
    for item in events:
        lines.append(f"• {_date_line(item['date'], include_year=False)} · {_time_line(item['date'], item.get('all_day'))} — {item['title']}")
    return "\n".join(lines)




def send_daily_birthdays(reference=None, thread_id=None, reply_markup=None, show_empty=True):
    reference = reference or _now()
    text = render_daily_birthdays(reference)
    if not text:
        if not show_empty:
            return None
        text = "🎈 aniversários de hoje\n\nnenhum aniversário para hoje."
    return send_message(GROUP_ID, text, thread_id=thread_id or THREADS["aniversarios"], reply_markup=reply_markup)


def send_daily_events(reference=None, thread_id=None, reply_markup=None, show_empty=True):
    reference = reference or _now()
    text = render_daily_events(reference)
    if not text:
        if not show_empty:
            return None
        text = "🗓️ agenda de hoje\n\nnenhum compromisso para hoje."
    return send_message(GROUP_ID, text, thread_id=thread_id or THREADS["agenda"], reply_markup=reply_markup)

def send_week_birthdays():
    return send_message(GROUP_ID, render_week_birthdays(), thread_id=THREADS["aniversarios"])


def send_week_events():
    return send_message(GROUP_ID, render_week_events(), thread_id=THREADS["agenda"])


def send_due_reminders():
    reference = _now()
    state = _load_state()
    _prune_state(state, reference)

    sent_count = 0
    day_key = reference.date().isoformat()

    birthday_text = render_daily_birthdays(reference)
    birthday_key = f"daily_birthdays:{day_key}"
    if birthday_text and not _already_sent(state, birthday_key):
        send_daily_birthdays(
            reference=reference,
            thread_id=THREADS["aniversarios"],
            reply_markup={
                "inline_keyboard": [[
                    {"text": "✅ li aniversários", "callback_data": "aniversarios_lidos"},
                    {"text": "🎈 ver semana", "callback_data": "aniversarios_semana"}
                ]]
            },
            show_empty=False
        )
        _mark_sent(state, birthday_key, reference)
        sent_count += 1

    events_text = render_daily_events(reference)
    events_key = f"daily_events:{day_key}"
    if events_text and not _already_sent(state, events_key):
        send_daily_events(
            reference=reference,
            thread_id=THREADS["agenda"],
            reply_markup={
                "inline_keyboard": [[
                    {"text": "✅ li agenda", "callback_data": "agenda_lida"},
                    {"text": "📅 ver semana", "callback_data": "agenda_semana"}
                ], [
                    {"text": "🔁 lembrar depois", "callback_data": "agenda_lembrar_depois"}
                ]]
            },
            show_empty=False
        )
        _mark_sent(state, events_key, reference)
        sent_count += 1

    if sent_count:
        state["last_daily_summary"] = reference.isoformat()
        _save_json(STATE_PATH, state, "🤖 registrar resumo diário enviado")

    return {"ok": True, "sent": sent_count}
