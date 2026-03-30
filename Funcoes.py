from Variaveis import *
import json
import os

ARQUIVO_SAVE ='save.json'

def salvar_jogo():
    dados= {
        "custo_prestigio": custo_prestigio,
        "custo_auto": custo_auto,
        "dinheiro": dinheiro,
        "dinheiro_por_clique": dinheiro_por_clique,
        "dinheiro_por_segundo": dinheiro_por_segundo,
        "custo_upgrade": custo_upgrade,
        "nivel_upgrade": nivel_upgrade,
        "nivel_prestigio": nivel_prestigio
    }
    with open(ARQUIVO_SAVE, "w") as arquivo:
        json.dump(dados, arquivo)

def carregar_jogo():
    global dinheiro, dinheiro_por_clique, dinheiro_por_segundo, custo_auto, custo_upgrade
    if os.path.exists(ARQUIVO_SAVE):
        with open(ARQUIVO_SAVE, 'r') as arquivo:
            dados = json.load(arquivo)
            
            dinheiro = dados.get("dinheiro", 0)
            dinheiro_por_clique = dados.get("dinheiro_por_clique", 1)
            dinheiro_por_segundo = dados.get("dinheiro_por_segundo", 0)
            custo_upgrade = dados.get("custo_upgrade", 10)
            custo_auto = dados.get("custo_auto", 50)
            nivel_upgrade = dados.get("nivel_upgrade", 1)
            nivel_prestigio = dados.get("nivel_prestigio", 0)
            custo_prestigio = dados.get("custo_prestigio", 100)

def realizar_prestigio():
    global dinheiro, dinheiro_por_clique, dinheiro_por_segundo, nivel_upgrade, custo_auto, nivel_prestigio, multiplicador_prestigio, custo_prestigio

    if dinheiro >= custo_prestigio:
        nivel_prestigio += 1
        bonus_atual = multiplicador_prestigio * nivel_prestigio

        dinheiro = 0
        dinheiro_por_clique = int(1 + bonus_atual)
        dinheiro_por_segundo = 0
        nivel_upgrade = 2
        custo_upgrade = 10
        custo_prestigio = int(custo_prestigio * 2)
        custo_auto = 50
        
        print(f"Prestígio nível {nivel_prestigio} alcançado!")
        salvar_jogo()