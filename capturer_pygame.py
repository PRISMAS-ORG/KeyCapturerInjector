import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura teclado - pygame")

print("Ventana activa necesaria para capturar teclado")
print("Pulsa ESC para salir")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print(f"Tecla presionada: {pygame.key.name(event.key)}")

        if event.type == pygame.KEYUP:
            print(f"Tecla soltada: {pygame.key.name(event.key)}")

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

pygame.quit()
sys.exit()