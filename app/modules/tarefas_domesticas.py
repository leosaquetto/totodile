from app.telegram_api import send_message
from app.constants import THREADS
from app.config import GROUP_ID

FIELDS = [
    ("cama", "cama"),
    ("louca", "louça"),
    ("banho", "banho"),
    ("dentes_manha", "dentes manhã"),
]


def render_text(state):
    lines = ["🏠 tarefas do dia", ""]
    for key, label in FIELDS:
        lines.append(f"{label}: {state.get(key, '❌')}")
    return "\n".join(lines)


def build_keyboard(state):
    buttons = []
    for key, label in FIELDS:
        status = state.get(key, "❌")
        buttons.append([{"text": f"{status} {label}", "callback_data": f"tarefa_{key}"}])
    return {"inline_keyboard": buttons}


def send_panel(state):
    return send_message(
        GROUP_ID,
        render_text(state),
        thread_id=THREADS["tarefas"],
        reply_markup=build_keyboard(state),
    )
