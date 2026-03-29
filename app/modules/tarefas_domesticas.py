from app.telegram_api import send_message
from app.constants import THREADS
from app.config import GROUP_ID

def render(data):
    return f"""
🐊 tarefas do dia

🛏️ cama: {data.get("cama","❌")}
🍽️ louça: {data.get("louca","❌")}
🚿 banho: {data.get("banho","❌")}
🦷 dentes manhã: {data.get("dentes_manha","❌")}
""".strip()

def send_panel(data):
    return send_message(
        GROUP_ID,
        render(data),
        thread_id=THREADS["tarefas"]
    )
