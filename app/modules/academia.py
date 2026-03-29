from app.telegram_api import send_message
from app.constants import THREADS
from app.config import GROUP_ID

def render(state):
    return f"""
🐊 academia

próximo treino: {state.get("proximo_treino","-")}
streak: {state.get("streak",0)}
último treino: {state.get("ultimo_treino","-")}
""".strip()

def send_academia(state):
    return send_message(
        GROUP_ID,
        render(state),
        thread_id=THREADS["academia"]
    )
