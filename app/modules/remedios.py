from app.telegram_api import send_message
from app.constants import THREADS
from app.config import GROUP_ID

def build_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "✅ tomei", "callback_data": "prep_ok"}],
            [{"text": "❌ não tomei", "callback_data": "prep_no"}],
            [{"text": "⏰ lembrar depois", "callback_data": "prep_later"}]
        ]
    }

def render_text(state):
    return f"""
🐊 remédio do dia

status: {state.get("status_hoje", "pendente")}
estoque: {state.get("estoque_atual", 0)} cápsulas
""".strip()

def send_prep(state):
    return send_message(
        GROUP_ID,
        render_text(state),
        thread_id=THREADS["remedios"],
        reply_markup=build_keyboard()
    )
