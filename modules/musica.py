import github_db

def formatar_nome_artista(nome):
    """Garante que o nome do artista só quebre linha após o SEGUNDO espaço."""
    partes = nome.split(" ")
    if len(partes) > 2:
        return f"{partes[0]} {partes[1]}\n{' '.join(partes[2:])}"
    return nome

async def comando_resumo_musica(update, context):
    # Aqui o bot lê o JSON que seus widgets do iOS jogaram no GitHub
    dados, _ = github_db.carregar_json("data/musica_stats.json")
    
    if not dados:
        await update.message.reply_text("🐊 Ainda não tenho dados de música sincronizados hoje!")
        return

    top_artistas = dados.get("top_artistas_hoje", [])
    
    texto = "🎧 *RESUMO MUSICAL DO DIA* 🎧\n\n"
    texto += "*Seus Artistas Mais Ouvidos:*\n"
    
    for i, artista in enumerate(top_artistas[:5], 1):
        nome_formatado = formatar_nome_artista(artista['nome']).replace('\n', ' ')
        texto += f"{i}. {nome_formatado} - {artista['minutos']} min\n"
        
    # Exemplo de lógica para o domingo (Ranking com os amigos)
    # Se hoje for domingo, ele anexa o ranking da semana:
    ranking_amigos = dados.get("ranking_semana", [])
    if ranking_amigos:
        texto += "\n🏆 *Ranking Semanal da Galera:*\n"
        # O ranking_amigos seria uma lista ordenada vinda do seu JSON com dados do Gab, Savio, Benny, Peter e você.
        for i, amigo in enumerate(ranking_amigos, 1):
            texto += f"{i}. {amigo['nome']} - {amigo['streams']} streams\n"

    await update.message.reply_text(texto, parse_mode="Markdown")
