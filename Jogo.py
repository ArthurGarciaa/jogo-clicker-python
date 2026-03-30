import pygame
import sys
import json
from Funcoes import *
from Variaveis import *
pygame.init()

# Janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Idle Game")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)

carregar_jogo()
salvar_jogo()
realizar_prestigio()

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
