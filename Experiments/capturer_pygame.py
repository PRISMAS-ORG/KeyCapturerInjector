import pygame
import sys,time


pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura teclado - pygame")

print("Ventana activa necesaria para capturar teclado")
print("Pulsa ESC para salir")

max_loop_time = 0
running = True
while running:
    #start = time.perf_counter()
    #if ahora - last_event >= 100:
        #send paquete
    #else:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            tecla = pygame.key.name(event.key)
            print(f"Tecla presionada: {tecla}")
            

        if event.type == pygame.KEYUP:
            tecla = pygame.key.name(event.key)
            print(f"Tecla soltada: {tecla}")

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print(f"Max loop time: {max_loop_time}")
            running = False
    end = time.perf_counter()
    loop_time = pygame.time.Clock().tick(1)
    #loop_time = end-start
    if loop_time>max_loop_time:
        max_loop_time = loop_time
    #print(f"Bucle en: {(end-start)*1000}")

pygame.quit()
sys.exit()

#El otro hilo
#while True:
    #if ahora - last_event >= 100:
        #send paquete
    #time.sleep(0.001)