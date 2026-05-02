from app.telegram_api import send_message
from app.constants import THREADS
from app.config import GROUP_ID


def render_text(state):
    return f"""
🏠 tarefas do dia

cama: {state.get('cama','❌')}
louça: {state.get('louca','❌')}
banho: {state.get('banho','❌')}
dentes manhã: {state.get('dentes_manha','❌')}
""".strip()


def send_panel(state):
    return send_message(
        GROUP_ID,
        render_text(state),
        thread_id=THREADS["tarefas"]
    )
