from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Simulando um banco de dados simples na memória (o ideal é ler/salvar no GitHub ou JSON)
estoque_prep = 14 

async def lembrete_prep(app, grupo_id):
    global estoque_prep
    teclado = [
        [InlineKeyboardButton("✅ Tomei", callback_data="prep_tomei")],
        [InlineKeyboardButton("❌ Não Tomei", callback_data="prep_nao_tomei")],
        [InlineKeyboardButton("⏰ Lembrar em 1h", callback_data="prep_lembrar")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    
    alerta_estoque = "🚨 Marque consulta na UBS! Seu estoque está acabando." if estoque_prep <= 5 else ""
    
    texto = (
        f"🐊 Bom dia! Hora do remédio.\n"
        f"💊 Estoque atual: {estoque_prep}/30\n"
        f"{alerta_estoque}"
    )
    
    # Substitua pelo ID do tópico de Remédios
    TOPICO_REMEDIOS_ID = 7 
    await app.bot.send_message(chat_id=grupo_id, message_thread_id=TOPICO_REMEDIOS_ID, text=texto, reply_markup=reply_markup)

async def handle_botoes_prep(update, context):
    query = update.callback_query
    await query.answer()
    
    global estoque_prep

    if query.data == "prep_tomei":
        estoque_prep -= 1
        await query.edit_message_text(text=f"✅ PrEP registrada! Estoque atualizado para {estoque_prep}/30. Bom garoto!")
        # Aqui você insere a lógica para salvar num log.json no GitHub
    elif query.data == "prep_nao_tomei":
        await query.edit_message_text(text="❌ Você marcou que não tomou. Tem certeza? Não vacila!")
    elif query.data == "prep_lembrar":
        await query.edit_message_text(text="⏰ Totodile vai te morder de novo em 1 hora!")
        # Lógica para reagendar no APScheduler iria aqui
