import pygame
import sys
import json
import os

pygame.init()

# Janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Idle Game")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)

ARQUIVO_SAVE ='save.json'

def salvar_jogo():
    dados= {
        "dinheiro": dinheiro,
        "dinheiro_por_clique": dinheiro_por_clique,
        "dinheiro_por_segundo": dinheiro_por_segundo,
        "custo_upgrade": custo_upgrade,
        "custo_auto": custo_auto,
        "nivel_upgrade": nivel_upgrade,
        "nivel_prestigio": nivel_prestigio,
        "custo_prestigio": custo_prestigio
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

# Estado do jogo
dinheiro = 0
dinheiro_por_clique = 1 
dinheiro_por_segundo = 0
nivel_upgrade = 1
custo_upgrade = 10
custo_auto = 50
multiplicador_prestigio = 1.5
nivel_prestigio = 0
custo_prestigio = 100
upgrade_auto = 0
custo_upgrade_auto = 50

botao_clique = pygame.Rect(300, 400, 200, 60)
botao_upgrade = pygame.Rect(300, 320, 200, 60)
ultimo_tempo = pygame.time.get_ticks()
botao_auto = pygame.Rect(300, 240, 200, 60)
botao_prestigio = pygame.Rect(300, 160, 200, 60)

rodando = True

carregar_jogo()
while rodando:
    agora = pygame.time.get_ticks()

    if agora - ultimo_tempo >= 1000:
        dinheiro += dinheiro_por_segundo
        ultimo_tempo = agora
        salvar_jogo()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            salvar_jogo()
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_clique.collidepoint(evento.pos):
                dinheiro += dinheiro_por_clique

            if botao_auto.collidepoint(evento.pos):
                if dinheiro >= custo_auto:
                    dinheiro -= custo_auto
                    dinheiro_por_segundo += 1
                    custo_auto = int (custo_auto * 1.5)

            if botao_upgrade.collidepoint(evento.pos):
                if dinheiro >= custo_upgrade:
                    dinheiro -= custo_upgrade
                    nivel_upgrade += 1
                    dinheiro_por_clique += 1
                    custo_upgrade = 5 * nivel_upgrade
            if botao_prestigio.collidepoint(evento.pos):
                realizar_prestigio()

    tela.fill((25, 25, 25))

    tela.blit(
        fonte.render(f"Money: {dinheiro}", True, (255, 255, 255)),
        (20, 20)
    )

    pygame.draw.rect(tela, (70, 130, 180), botao_clique)
    tela.blit(
        fonte.render(f"Click (+{dinheiro_por_clique})", True, (255, 255, 255)),
        fonte.render("x", True, (0,0,0)).get_rect(center=botao_clique.center)
    )

    cor_upgrade = (100, 100, 100) if dinheiro < custo_upgrade else (0, 150, 0)
    pygame.draw.rect(tela, cor_upgrade, botao_upgrade)

    tela.blit(
        fonte.render(f"Upgrade Lv.{nivel_upgrade} - ${custo_upgrade}", True, (255, 255, 255)),
        fonte.render("x", True, (0,0,0)).get_rect(center=botao_upgrade.center)
    )

    cor_auto = (100, 100, 100) if dinheiro < custo_auto else (180, 120, 0)
    pygame.draw.rect(tela, cor_auto, botao_auto)

    texto_auto = fonte.render(
        f"Auto +1/s - ${custo_auto}",
    True, (255, 255, 255)
    )
    tela.blit(texto_auto, texto_auto.get_rect(center=botao_auto.center))

    cor_prestigio = (200, 0, 200) if dinheiro >= custo_prestigio else (80, 0, 80)
    pygame.draw.rect(tela, cor_prestigio, botao_prestigio)

    texto_prestigio = fonte.render (f"PRESTÍGIO - ${custo_prestigio}", True, (255, 255, 255))
    tela.blit(texto_prestigio, texto_prestigio.get_rect(center = botao_prestigio.center))

    tela.blit(fonte.render(f"Nível de prestígio: {nivel_prestigio}", True, (200, 200, 200)), (20, 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
