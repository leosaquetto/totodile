# Como você não tem horário fixo para treinar dependendo das gravações pro Privacy/OnlyFans,
# O Totodile pode ser acionado via comando ou enviar um resumo no início do dia.

async def registrar_peso(update, context):
    # Exemplo de comando: /peso 72.5
    try:
        peso = float(context.args[0])
        falta = 82.0 - peso
        texto = f"💪🏼 Peso registrado: {peso}kg.\nFaltam {falta:.1f}kg para a meta de 82kg. Bora amassar na SmartFit!"
        await update.message.reply_text(texto)
    except:
        await update.message.reply_text("Use o formato: /peso 72.5")
