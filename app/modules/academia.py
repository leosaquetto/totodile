from app.telegram_api import send_message
from app.constants import THREADS
from app.config import GROUP_ID


def render_text(state):
    return f"""
🏋️ academia

próximo treino: {state.get('proximo_treino','-')}
streak: {state.get('streak',0)} dias
último treino: {state.get('ultimo_treino','-')}
""".strip()


def build_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "✅ fiz treino", "callback_data": "academia_done"},
                {"text": "⏭️ pulei", "callback_data": "academia_skip"},
            ]
        ]
    }


def send_academia(state):
    return send_message(
        GROUP_ID,
        render_text(state),
        thread_id=THREADS["academia"],
        reply_markup=build_keyboard(),
    )
