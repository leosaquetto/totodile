from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def enviar_checklist(app, grupo_id):
    # Como sua rotina de criação de conteúdo varia, o checklist não julga o horário.
    teclado = [
        [InlineKeyboardButton("🛏️ Cama (Pendente)", callback_data="tarefa_cama")],
        [InlineKeyboardButton("🍽️ Louça (Pendente)", callback_data="tarefa_louca")],
        [InlineKeyboardButton("🚿 Banho (Pendente)", callback_data="tarefa_banho")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    TOPICO_TAREFAS_ID = 8
    await app.bot.send_message(
        chat_id=grupo_id, 
        message_thread_id=TOPICO_TAREFAS_ID, 
        text="🐊 E aí, como foi a organização hoje? Marca aí o que já fez:", 
        reply_markup=reply_markup
    )

async def handle_botoes_tarefas(update, context):
    query = update.callback_query
    await query.answer()
    
    # Aqui o ideal é ler os botões atuais da mensagem e alterar apenas o que foi clicado.
    # Exemplo simplificado:
    if query.data == "tarefa_cama":
        await query.edit_message_text(text="✅ Cama arrumada registrada!")
