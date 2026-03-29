from app.modules import remedios, tarefas_domesticas, academia

def run():
    remedios.send_prep({
        "status_hoje": "pendente",
        "estoque_atual": 64
    })

    tarefas_domesticas.send_panel({
        "cama": "❌",
        "louca": "❌",
        "banho": "✅",
        "dentes_manha": "✅"
    })

    academia.send_academia({
        "proximo_treino": "treino a",
        "streak": 4,
        "ultimo_treino": "ontem"
    })

if __name__ == "__main__":
    run()
