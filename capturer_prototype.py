import pygame, socket, struct
import sys,time,json

SERVER_IP = '192.168.1.113'#'127.0.0.1'  #'192.168.1.113'#'80.28.209.181'  # IP del servidor
PORT = 8082
SEND_RATE_HZ = 30           # Frecuencia de envío UDP
DEADZONE = 0.1               # Zona muerta para joysticks
MOUSE_DEADZONE = 0

CAPTURE_KEYS = True
CAPTURE_GAMEPAD = True
CAPTURE_MOUSE = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER_IP,PORT)

'''
provisional packet
w,a,s,d,e,r,q,up,down,left,right,space,enter,shift_l,ctrl_l,esc
ejes mando: axes[0], axes[1], axes[2], axes[3]
16 botones
dpad o pov (flechas direccion del mando): dos bytes
3 botones raton: 3 bytes
2 int para movimiento relativo (son 4 bytes cada uno con signo, a veces da -1)
tam: 69Bytes
'''
packet_format = ">16B6f16B2b3B2i"
teclas_list = ["w","a","s","d","e","r","q","up","down","left","right"\
,"space","return","left shift","left ctrl","escape"]
teclas_packet = [0]*16
axes = [0.0]*6  # Left stick X/Y, Right stick X/Y
last_axes = [0.0]*6
buttons = [0] * 16           # 16 botones
dpad = [0] * 2
mouse_buttons = [0]*3
mouse_rel_pos = [0]*2


pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Captura teclado - pygame")

print("Ventana activa necesaria para capturar teclado")
print("Pulsa ESC para salir")

#Config mouse
pygame.event.set_grab(True)        # Captura el ratón dentro de la ventana
pygame.mouse.set_visible(True)    # Oculta el cursor
center = (200, 100)
pygame.mouse.set_pos(center)

#Detectar joystick
if pygame.joystick.get_count() > 0:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print("Joystick detectado:", joy.get_name())
    print(joy.get_numaxes())
else:
    joy = None
    print("No hay joystick, usando teclado solamente")

#Preparar reloj
clock = pygame.time.Clock()
max_loop_time = 0
running = True

#Bucle de juego
while running:
    for event in pygame.event.get():
        #Eventos de teclas
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

        #Eventos de mando
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

        #Eventos de raton
        if event.type == pygame.MOUSEBUTTONDOWN:
            boton_mouse = event.button-1
            if boton_mouse < 3:
                mouse_buttons[boton_mouse] = 1
        if event.type == pygame.MOUSEBUTTONUP:
            boton_mouse = event.button-1
            if boton_mouse < 3:
                mouse_buttons[boton_mouse]= 0

        #Eventos de salida: escape, o cerrar ventana
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    #Ejes joystick por polling
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

    #Posicion relativa raton
    new_mouse_x,new_mouse_y = pygame.mouse.get_rel()
    if abs(mouse_rel_pos[0] - new_mouse_x) > MOUSE_DEADZONE or abs(mouse_rel_pos[1] - new_mouse_y) > MOUSE_DEADZONE:
        mouse_rel_pos[0] = new_mouse_x
        mouse_rel_pos[1] = new_mouse_y
    pygame.mouse.set_pos(center)

    #Envio de paquete de estado 
    packet = struct.pack(packet_format,*teclas_packet,*axes,*buttons,*dpad,*mouse_buttons, *mouse_rel_pos)
    sock.sendto(packet, (SERVER_IP, PORT))
    print(f"Paquete: {struct.unpack(packet_format, packet)}", end="\r")

    #Final del bucle de juego
    pygame.display.flip() #No es obligatorio porque no dibujamos nada, solo recomendable
    loop_time = clock.tick(SEND_RATE_HZ)

pygame.quit()
sys.exit()

#El otro hilo
#while True:
    #if ahora - last_event >= 100:
        #send paquete
    #time.sleep(0.001)