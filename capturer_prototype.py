import pygame, socket, struct
import sys,time,json


# =========================
# CONFIGURACIÓN
# =========================
SERVER_IP = '192.168.1.113'#'127.0.0.1'  #'192.168.1.113'#'80.28.209.181'  # IP del servidor
PORT = 8082
SEND_RATE_HZ = 30           # Frecuencia de envío UDP
DEADZONE = 0.1               # Zona muerta para joysticks

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER_IP,PORT)

'''
provisional packet
w,a,s,d,e,r,q,up,down,left,right,space,enter,shift_l,ctrl_l,esc
ejes mando: axes[0], axes[1], axes[2], axes[3]
16 botones
'''
packet_format = ">16B6f16B2b"
teclas_list = ["w","a","s","d","e","r","q","up","down","left","right"\
,"space","return","left shift","left ctrl","escape"]
teclas_packet = [0]*16
axes = [0.0]*6  # Left stick X/Y, Right stick X/Y
last_axes = [0.0]*6
buttons = [0] * 16           # 16 botones
dpad = [0] * 2


pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura teclado - pygame")

print("Ventana activa necesaria para capturar teclado")
print("Pulsa ESC para salir")


#Detectar joystick
if pygame.joystick.get_count() > 0:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print("Joystick detectado:", joy.get_name())
    print(joy.get_numaxes())
else:
    joy = None
    print("No hay joystick, usando teclado solamente")


max_loop_time = 0
running = True
while running:
    #if ahora - last_event >= 100:
        #send paquete
    #else:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            tecla = pygame.key.name(event.key)
            #print(f"Tecla presionada: {tecla}")
            if tecla in teclas_list:
                teclas_packet[teclas_list.index(tecla)] = 1

        if event.type == pygame.KEYUP:
            tecla = pygame.key.name(event.key)
            #print(f"Tecla soltada: {tecla}")
            if tecla in teclas_list:
                teclas_packet[teclas_list.index(tecla)] = 0

        if event.type == pygame.JOYBUTTONDOWN:
            boton = event.button
            #print(f"boton pulsado:{boton}")
            buttons[boton] = 1

        if event.type == pygame.JOYBUTTONUP:
            boton = event.button
            #print(f"boton soltado:{boton}") 
            buttons[boton] = 0

        if event.type == pygame.JOYHATMOTION:
            # event.value contiene la tupla (x, y)
            dpad[0] = event.value[0]
            dpad[1] = event.value[1]

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    if joy:
        # Ejes
        for i in range(min(4, joy.get_numaxes())):
            val = joy.get_axis(i)
            if abs(val) < DEADZONE:
                val = 0.0
            axes[i] = val
            # DEBUG solo si cambia se printa
            if round(val, 2) != round(last_axes[i], 2):
                #print(f"Eje {i}: {val:.2f}")
                last_axes[i] = val

    #print(teclas_packet)
    packet = struct.pack(packet_format,*teclas_packet,*axes,*buttons,*dpad)
    sock.sendto(packet, (SERVER_IP, PORT))
    print(f"Paquete: {struct.unpack(packet_format, packet)}", end="\r")
    #print(*dpad)
    loop_time = pygame.time.Clock().tick(SEND_RATE_HZ)

pygame.quit()
sys.exit()

#El otro hilo
#while True:
    #if ahora - last_event >= 100:
        #send paquete
    #time.sleep(0.001)