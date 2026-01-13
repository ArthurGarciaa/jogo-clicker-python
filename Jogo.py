import pygame
import sys

pygame.init()

# Janela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Idle Game")

clock = pygame.time.Clock()

fonte = pygame.font.SysFont(None, 36)

dinheiro = 0
dinheiro_por_clique = 1
custo_upgrade = 10
upgrade = 1

botao_rect = pygame.Rect(300, 400, 200, 60)
botao_upgrade = pygame.Rect(300, 320, 200, 60)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if botao_rect.collidepoint(evento.pos):
                dinheiro += 1
            if botao_upgrade.collidepoint(evento.pos):
                if dinheiro >= custo_upgrade:
                    dinheiro -= custo_upgrade
                    upgrade += 1
                    dinheiro_por_clique = upgrade
                    custo_upgrade = int(upgrade * 2)

    tela.fill((25, 25, 25))

    texto_dinheiro = fonte.render(f"Dinheiro: {int(dinheiro)}", True, (255, 255, 255))
    tela.blit(texto_dinheiro, (20,20))

    pygame.draw.rect(tela, (70, 130, 180), botao_rect)
    texto_botao = fonte.render("Ganhar +1", True, (255,255,255))
    tela.blit(texto_botao, texto_botao.get_rect(center=botao_rect.center))

    cor_upgrade = (100, 100, 100) if dinheiro < custo_upgrade else (0, 150, 0)

    pygame.draw.rect(tela, cor_upgrade, botao_upgrade)
    texto_upgrade = fonte.render(f"Upgrade (+1) - ${custo_upgrade}", True, (255, 255, 255))
    tela.blit(texto_upgrade, texto_upgrade.get_rect(center=botao_upgrade.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
