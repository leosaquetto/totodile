import os
import requests
from datetime import datetime

# Se você for usar o GitHub para armazenar o TXT, precisaremos do token para ler.
# Aqui vamos simular a leitura do arquivo txt que você faz no JS.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "leosaquetto"
REPO_NAME = "totodile"
FILE_PATH = "data/historico_treinos.txt" # Onde o master widget salva no github

def ler_historico_treinos():
    """
    Simula a função loadHistoryFile() do seu Scriptable.
    Lê o arquivo TXT e transforma numa lista de dicionários.
    """
    # Exemplo prático de como puxar do GitHub (requer token configurado no .env)
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.text
        else:
            # Fallback temporário para testes locais
            with open("historico_treinos.txt", "r", encoding="utf-8") as f:
                content = f.read()
    except Exception:
        return []

    linhas = [l.strip() for l in content.split("\n") if l.strip()]
    registros = []
    
    for linha in linhas:
        partes = [p.strip() for p in linha.split("|")]
        if len(partes) >= 3:
            try:
                # Converte DD/MM/AAAA para objeto datetime do Python
                data_obj = datetime.strptime(partes[0], "%d/%m/%Y")
                registros.append({
                    "data_str": partes[0],
                    "data": data_obj,
                    "dia_semana": partes[1],
                    "treino": partes[2]
                })
            except ValueError:
                continue
                
    return registros

def calcular_streak_e_gap(registros):
    """
    Tradução exata do seu calculateStreak() e calculateDaysWithoutTraining().
    """
    if not registros:
        return 0, 0
        
    datas = sorted([r["data"] for r in registros])
    hoje = datetime.now()
    ultimo_treino = datas[-1]
    
    # Gap em dias
    gap = (hoje.date() - ultimo_treino.date()).days
    
    # Streak
    streak = 1
    for i in range(len(datas) - 1, 0, -1):
        diff = (datas[i].date() - datas[i - 1].date()).days
        if diff == 1:
            streak += 1
        else:
            break
            
    # Sua regra: streak só zera se o gap for >= 2
    if gap >= 2:
        streak = 0
        
    return streak, gap

def treinos_no_mes(registros):
    """Tradução do monthStats()."""
    hoje = datetime.now()
    treinos_mes = set()
    
    for r in registros:
        d = r["data"]
        if d.month == hoje.month and d.year == hoje.year:
            treinos_mes.add(r["data_str"])
            
    return len(treinos_mes)

def descobrir_proximo_treino(registros):
    """
    Tradução do findOldestWorkout().
    Acha o treino que foi feito há mais tempo baseado na letra (A1, B2, etc).
    """
    mapa_ultimos = {}
    
    for r in registros:
        # Pega só a chave curta antes do parênteses. Ex: "A1 (Peito..." -> "A1"
        chave_curta = r["treino"].split("(")[0].strip()
        
        if chave_curta not in mapa_ultimos or r["data"] > mapa_ultimos[chave_curta]["data"]:
            mapa_ultimos[chave_curta] = r
            
    if not mapa_ultimos:
        return None
        
    # Pega o que tem a data mais antiga entre os últimos feitos
    treino_mais_antigo = min(mapa_ultimos.values(), key=lambda x: x["data"])
    return treino_mais_antigo["treino"]

async def comando_treino(update, context):
    """
    Comando /treino no Telegram que responde com o status completo.
    """
    registros = ler_historico_treinos()
    
    if not registros:
        await update.message.reply_text("🐊 Sem registros de treino encontrados!")
        return

    streak, gap = calcular_streak_e_gap(registros)
    qtd_mes = treinos_no_mes(registros)
    proximo = descobrir_proximo_treino(registros)
    
    ultimo = registros[-1]
    
    # Formata a mensagem do Totodile
    texto = "🏋🏻‍♂️ *RESUMO DE TREINOS DO TOTODILE* 🏋🏻‍♂️\n\n"
    
    # Streak / Gap
    if gap <= 1:
        texto += f"🏆 *Streak:* {streak} dias seguidos! Mandou bem!\n"
    else:
        texto += f"🚨 *Atenção:* Você está há {gap} dias sem treinar! Bora pra SmartFit!\n"
        
    texto += f"📅 *Treinos neste mês:* {qtd_mes}\n\n"
    
    # Status de hoje/amanhã
    if gap == 0:
        texto += "✅ *Status:* Treinado HOJE!\n"
        texto += f"⏭️ *Próximo treino (Amanhã):*\n{proximo}\n\n"
    else:
        texto += "⏳ *Status:* Fazer HOJE!\n"
        texto += f"⏭️ *Seu treino hoje será:*\n{proximo}\n\n"
        
    texto += f"🔄 *Último registrado:* {ultimo['dia_semana']} ({ultimo['data_str']}) - {ultimo['treino']}"
    
    await update.message.reply_text(texto, parse_mode="Markdown")
