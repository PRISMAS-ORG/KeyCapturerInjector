import pygame
import sys,time


pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura raton - pygame")

print("Ventana activa necesaria para capturar raton")
print("Pulsa ESC para salir")


mouse_x,mouse_y = 0,0
mouse_deadzone = 0

pygame.event.set_grab(True)        # Captura el ratón dentro de la ventana
#pygame.mouse.set_visible(False)    # Oculta el cursor
center = (200, 100)
pygame.mouse.set_pos(center)


max_loop_time = 0
clock = pygame.time.Clock()
running = True
while running:
    #pygame.mouse.set_pos(200,100)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
           print(f"Wheel {event}")
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Buttondown {event.button}")
        if event.type == pygame.MOUSEBUTTONUP:
            print(f"ButtonUP {event.button}")
        #if event.type == pygame.MOUSEMOTION:
        #    print(f"Movimiento: {event}")
        #if event.type == pygame.MOUSEMOTION:
        #    dx, dy = event.rel
        #    print(dx, dy)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print(f"Max loop time: {max_loop_time}")
            running = False

    new_mouse_x,new_mouse_y = pygame.mouse.get_rel()
    if abs(mouse_x - new_mouse_x) > mouse_deadzone or abs(mouse_y - new_mouse_y) > mouse_deadzone:
        mouse_x = new_mouse_x
        mouse_y = new_mouse_y
        print(f"Mouse: {mouse_x},{mouse_y}")
    pygame.mouse.set_pos(center)
    pygame.display.flip()

    loop_time = clock.tick(60)
    
    if loop_time>max_loop_time:
        max_loop_time = loop_time
    #print(f"Bucle en: {loop_time}")

pygame.quit()
sys.exit()

#El otro hilo
#while True:
    #if ahora - last_event >= 100:
        #send paquete
    #time.sleep(0.001)