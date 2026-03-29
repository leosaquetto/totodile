import os
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Importando os módulos
from modules import remedios_saude, academia, tarefas_casa

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GRUPO_ID = os.getenv("GRUPO_ID")

async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Totodile pronto pra morder a procrastinação! 🐊💧"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    scheduler = AsyncIOScheduler()

    # Comandos Básicos
    app.add_handler(CommandHandler("start", start))

    # Handlers dos Módulos (Callbacks de botões)
    app.add_handler(CallbackQueryHandler(remedios_saude.handle_botoes_prep, pattern="^prep_"))
    app.add_handler(CallbackQueryHandler(tarefas_casa.handle_botoes_tarefas, pattern="^tarefa_"))

    # Agendamentos (Cron Jobs) - Horários de Brasília
    # Remédio PrEP às 09:00
    scheduler.add_job(remedios_saude.lembrete_prep, 'cron', hour=9, minute=0, args=[app, GRUPO_ID])
    
    # Checklist flexível no fim da tarde (ex: 18:00) 
    scheduler.add_job(tarefas_casa.enviar_checklist, 'cron', hour=18, minute=0, args=[app, GRUPO_ID])

    scheduler.start()
    print("Totodile está online!")
    app.run_polling()

if __name__ == '__main__':
    main()
