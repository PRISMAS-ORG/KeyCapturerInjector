import pygame, socket
import sys,time,json

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('192.168.1.113',5001)

packet = {"key":None,
        "action": None,
        "value": None}


pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura teclado - pygame")

print("Ventana activa necesaria para capturar teclado")
print("Pulsa ESC para salir")

running = True
while running:
    start = time.perf_counter()
    #if ahora - last_event >= 100:
        #send paquete
    #else:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            tecla = pygame.key.name(event.key)
            print(f"Tecla presionada: {tecla}")
            #envias
            packet["key"]=tecla
            packet["action"] = "pressed"
            message = json.dumps(packet).encode('utf-8')
            socket.sendto(message,server_address)
            #last_event=ahora_mismo

        if event.type == pygame.KEYUP:
            tecla = pygame.key.name(event.key)
            print(f"Tecla soltada: {tecla}")
            #envias
            packet["key"]=tecla
            packet["action"] = "released"
            message = json.dumps(packet).encode('utf-8')
            socket.sendto(message,server_address)
            #last_event=ahora_mismo

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #envias
            packet["key"]=tecla
            packet["action"] = "released"
            message = json.dumps(packet).encode('utf-8')
            socket.sendto(message,server_address)
            #last_event=ahora_mismo
            running = False

    end = time.perf_counter()
    #pygame.time.Clock().tick(60)
    #print(f"Bucle en: {(end-start)*1000}")

pygame.quit()
sys.exit()

#El otro hilo
#while True:
    #if ahora - last_event >= 100:
        #send paquete
    #time.sleep(0.001)