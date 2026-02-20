import pygame
import sys,time, threading
from pynput import keyboard


pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura teclado - pygame")

print("Ventana activa necesaria para capturar teclado")
print("Pulsa ESC para salir")

pynput_pulsed = 0
pynput_released = 0
released = 0
pulsed = 0

def on_press(key):
    pynput_pulsed = time.perf_counter()
    try:
        print(f"    [PYNPUT] Tecla presionada: {key.char}:{pynput_pulsed}")
    except AttributeError:
        print(f"    [PYNPUT] Tecla presionada: {key}:{pynput_pulsed}")

def on_release(key):
    pynput_released = time.perf_counter()
    print(f"    [PYNPUT] Tecla soltada: {key}:{pynput_released}")
    
    # Salir con ESC
    if key == keyboard.Key.esc:
        print("Saliendo...")
        return False

print("Escuchando teclado globalmente... (ESC para salir)")

def capturer_pynput():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

def capturer_pygame():
    running = True
    while running:
        start = time.perf_counter()
        #if ahora - last_event >= 100:
            #send paquete
        #else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                tecla = pygame.key.name(event.key)
                pulsed = time.perf_counter()
                print(f"[PYGAME] Tecla presionada: {tecla}:{pulsed}")
                

            if event.type == pygame.KEYUP:
                tecla = pygame.key.name(event.key)
                released = time.perf_counter()
                print(f"[PYGAME] Tecla soltada: {tecla}:{released}")

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        end = time.perf_counter()
        #pygame.time.Clock().tick(60)
        #print(f"Bucle en: {(end-start)*1000}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("Test captura")
    #hilo_pygame = threading.Thread(target=capturer_pygame, daemon=True)
    hilo_pynput = threading.Thread(target=capturer_pynput, daemon=True)
    #hilo_pygame.start()
    hilo_pynput.start()
    capturer_pygame()