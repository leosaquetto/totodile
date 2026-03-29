from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
import github_db

ARQUIVO_PREP = "data/prep_log.json"

async def lembrete_prep(app, grupo_id):
    dados, _ = github_db.carregar_json(ARQUIVO_PREP)
    estoque = dados.get("estoque", 90) # Supondo 3 potinhos iniciais
    
    teclado = [
        [InlineKeyboardButton("✅ Tomei", callback_data="prep_tomei"),
         InlineKeyboardButton("❌ Não Tomei", callback_data="prep_nao_tomei")],
        [InlineKeyboardButton("⏰ Lembrar mais tarde", callback_data="prep_lembrar")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    
    # Alerta crítico de 1 potinho restante (30 dias)
    alerta = "\n\n🚨 **ATENÇÃO:** Só resta 1 potinho (30 dias)! Agende a UBS para os exames rápidos e renovar a receita." if estoque <= 30 else ""
    
    texto = f"🐊 Bom dia! Hora da PrEP.\n💊 Estoque atual: {estoque} cápsulas.{alerta}"
    await app.bot.send_message(chat_id=grupo_id, message_thread_id=7, text=texto, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_botoes_prep(update, context):
    query = update.callback_query
    await query.answer()
    
    dados, sha = github_db.carregar_json(ARQUIVO_PREP)
    estoque = dados.get("estoque", 90)
    log_mensal = dados.get("log", {})
    hoje = datetime.now().strftime("%Y-%m-%d")

    if query.data == "prep_tomei":
        estoque -= 1
        log_mensal[hoje] = "✅"
        dados["estoque"] = estoque
        dados["log"] = log_mensal
        github_db.salvar_json(ARQUIVO_PREP, dados, sha)
        await query.edit_message_text(text=f"✅ PrEP registrada! Estoque: {estoque}. Log salvo no GitHub.")
        
    elif query.data == "prep_nao_tomei":
        log_mensal[hoje] = "❌"
        dados["log"] = log_mensal
        github_db.salvar_json(ARQUIVO_PREP, dados, sha)
        await query.edit_message_text(text="❌ Marcado como NÃO tomado no log. Foco na saúde, não vacila amanhã!")
