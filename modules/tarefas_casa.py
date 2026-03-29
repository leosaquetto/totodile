from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import github_db

async def enviar_checklist(app, grupo_id):
    hoje = datetime.now().strftime("%Y-%m-%d")
    ARQUIVO_TAREFAS = f"data/habitos_{datetime.now().strftime('%Y_%m')}.json"
    
    dados, sha = github_db.carregar_json(ARQUIVO_TAREFAS)
    if hoje not in dados:
        dados[hoje] = {
            "cama": "❌", "louca": "❌", "banho": "❌", "proteina": "❌",
            "dente_m": "❌", "dente_t": "❌", "dente_n": "❌", "almoco": "❌", "jantar": "❌"
        }
        github_db.salvar_json(ARQUIVO_TAREFAS, dados, sha)

    h = dados[hoje]
    
    teclado = [
        [InlineKeyboardButton(f"🛏️ Cama: {h['cama']}", callback_data="hab_cama"),
         InlineKeyboardButton(f"🍽️ Louça: {h['louca']}", callback_data="hab_louca")],
        [InlineKeyboardButton(f"🦷 Dente (M): {h['dente_m']}", callback_data="hab_dente_m"),
         InlineKeyboardButton(f"🦷 Dente (T): {h['dente_t']}", callback_data="hab_dente_t"),
         InlineKeyboardButton(f"🦷 Dente (N): {h['dente_n']}", callback_data="hab_dente_n")],
        [InlineKeyboardButton(f"🍱 Almoço: {h['almoco']}", callback_data="hab_almoco"),
         InlineKeyboardButton(f"🍲 Jantar: {h['jantar']}", callback_data="hab_jantar")],
        [InlineKeyboardButton(f"🚿 Banho: {h['banho']}", callback_data="hab_banho"),
         InlineKeyboardButton(f"🥩 Proteína (Pós-treino): {h['proteina']}", callback_data="hab_proteina")]
    ]
    
    reply_markup = InlineKeyboardMarkup(teclado)
    await app.bot.send_message(
        chat_id=grupo_id, message_thread_id=8, 
        text=f"🐊 Status das Tarefas de Hoje ({hoje}):\nClique para alternar entre feito e não feito!", 
        reply_markup=reply_markup
    )

async def handle_botoes_tarefas(update, context):
    query = update.callback_query
    tarefa_key = query.data.replace("hab_", "")
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    ARQUIVO_TAREFAS = f"data/habitos_{datetime.now().strftime('%Y_%m')}.json"
    
    dados, sha = github_db.carregar_json(ARQUIVO_TAREFAS)
    h = dados.get(hoje, {})
    
    # Alterna o status
    h[tarefa_key] = "✅" if h.get(tarefa_key) == "❌" else "❌"
    dados[hoje] = h
    github_db.salvar_json(ARQUIVO_TAREFAS, dados, sha)
    
    # Reconstrói o teclado atualizado (mesma estrutura acima)
    teclado = [
        [InlineKeyboardButton(f"🛏️ Cama: {h['cama']}", callback_data="hab_cama"),
         InlineKeyboardButton(f"🍽️ Louça: {h['louca']}", callback_data="hab_louca")],
        [InlineKeyboardButton(f"🦷 Dente (M): {h['dente_m']}", callback_data="hab_dente_m"),
         InlineKeyboardButton(f"🦷 Dente (T): {h['dente_t']}", callback_data="hab_dente_t"),
         InlineKeyboardButton(f"🦷 Dente (N): {h['dente_n']}", callback_data="hab_dente_n")],
        [InlineKeyboardButton(f"🍱 Almoço: {h['almoco']}", callback_data="hab_almoco"),
         InlineKeyboardButton(f"🍲 Jantar: {h['jantar']}", callback_data="hab_jantar")],
        [InlineKeyboardButton(f"🚿 Banho: {h['banho']}", callback_data="hab_banho"),
         InlineKeyboardButton(f"🥩 Proteína: {h['proteina']}", callback_data="hab_proteina")]
    ]
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(teclado))
