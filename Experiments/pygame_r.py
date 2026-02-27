# import pygame
# import socket
# import struct
# import time
# import sys

# # =========================
# # CONFIGURACIÓN
# # =========================
# SERVER_IP = '80.28.209.181'   # Cambia por IP del servidor
# PORT = 8081
# SEND_RATE_HZ = 250        # Frecuencia de envío
# DEADZONE = 0.05           # Deadzone para los ejes. Zona muerta alrededor del centro del joystick

# # =========================
# # INICIALIZACIÓN
# # =========================
# pygame.init()
# pygame.joystick.init()

# # Crear ventana obligatoria para capturar teclado
# screen = pygame.display.set_mode((400, 200))
# pygame.display.set_caption("Cliente Control - Pygame")

# clock = pygame.time.Clock() # Controla la frecuencia del loop
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket UDP

# # =========================
# # JOYSTICK
# # =========================
# if pygame.joystick.get_count() > 0:
    # joy = pygame.joystick.Joystick(0)
    # joy.init()
    # print("Joystick detectado:", joy.get_name())
# else:
    # joy = None
    # print("No hay joystick, usando teclado.")

# print("Haz CLICK dentro de la ventana para capturar teclado.")

# # =========================
# # ESTADO INTERNO
# # =========================
# axes = [0.0, 0.0, 0.0, 0.0] # Lista de ejes [x-left, y-left, x-right, y-right]
# buttons = [0] * 16          # Lista de botones 16 bits

# # Variables para debug
# last_axes = [0.0] * 4   # almacenar último valor eje
# last_buttons = [0] * 16 # almacenar último estado botón

# # =========================
# # BUCLE PRINCIPAL
# # =========================
# running = True

# while running:

    # # -------------------------
    # # Procesar eventos
    # # -------------------------
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
            # running = False

        # # Manejo por eventos teclado
        # if event.type == pygame.KEYDOWN:
            # key = pygame.key.name(event.key)
            # if event.key == pygame.K_a:
                # axes[0] = -1.0
                # print(f"Tecla presionada: {key}")
            # if event.key == pygame.K_d:
                # axes[0] = 1.0
                # print(f"Tecla presionada: {key}")
            # if event.key == pygame.K_w:
                # axes[1] = -1.0
                # print(f"Tecla presionada: {key}")
            # if event.key == pygame.K_s:
                # axes[1] = 1.0
                # print(f"Tecla presionada: {key}")
            # if event.key == pygame.K_SPACE:
                # buttons[0] = 1
                # print(f"Tecla presionada: {key}")

        # if event.type == pygame.KEYUP:
            # key = pygame.key.name(event.key)
            # if event.key in (pygame.K_a, pygame.K_d):
                # axes[0] = 0.0
                # print(f"Tecla liberada: {key}")
            # if event.key in (pygame.K_w, pygame.K_s):
                # axes[1] = 0.0
                # print(f"Tecla liberada: {key}")
            # if event.key == pygame.K_SPACE:
                # buttons[0] = 0
                # print(f"Tecla liberada: {key}")

    # # -------------------------
    # # JOYSTICK (si existe)
    # # -------------------------
    # if joy:
        # for i in range(min(4, joy.get_numaxes())):
            # val = joy.get_axis(i)

            # # Deadzone
            # if abs(val) < DEADZONE:
                # val = 0.0

            # axes[i] = val

            # # DEBUG eje
            # if round(val, 2) != round(last_axes[i], 2):
                # print(f"Eje {i}: {val:.2f}")
                # last_axes[i] = val

        # for i in range(min(16, joy.get_numbuttons())):
            # val = joy.get_button(i)
            # buttons[i] = val

            # # DEBUG botón
            # if val != last_buttons[i]:
                # estado = "Presionado" if val else "Liberado"
                # print(f"Botón {i}: {estado}")
                # last_buttons[i] = val

    # # -------------------------
    # # EMPAQUETADO
    # # -------------------------
    # timestamp = time.time()

    # packet = struct.pack(
        # "d4f16B", # Formato: double (timestamp) + 4 floats (4 ejes del joystick normalizados) + 16 bytes (16 botones)
        # timestamp,
        # axes[0], axes[1], axes[2], axes[3],
        # *buttons
    # )

    # # Enviar UDP
    # sock.sendto(packet, (SERVER_IP, PORT))

    # # Limitar frecuencia
    # clock.tick(SEND_RATE_HZ)

# # =========================
# # SALIDA LIMPIA
# # =========================
# pygame.quit()
# sys.exit()





# import pygame
# import socket
# import struct
# import time
# import sys

# # =========================
# # CONFIGURACIÓN
# # =========================
# SERVER_IP = '80.28.209.181'  # IP del servidor
# PORT = 8081
# SEND_RATE_HZ = 250           # Frecuencia de envío UDP
# DEADZONE = 0.1               # Zona muerta para joysticks

# # =========================
# # INICIALIZACIÓN PYGAME
# # =========================
# pygame.init()
# pygame.joystick.init()

# # Crear ventana (obligatoria para capturar teclado)
# screen = pygame.display.set_mode((400, 200))
# pygame.display.set_caption("Cliente Control - Pygame")

# clock = pygame.time.Clock()
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # =========================
# # DETECCIÓN DE JOYSTICK
# # =========================
# if pygame.joystick.get_count() > 0:
    # joy = pygame.joystick.Joystick(0)
    # joy.init()
    # print("Joystick detectado:", joy.get_name())
# else:
    # joy = None
    # print("No hay joystick, usando teclado solamente")

# print("Haz CLICK dentro de la ventana para capturar teclado.")

# # =========================
# # ESTADO INTERNO
# # =========================
# axes = [0.0, 0.0, 0.0, 0.0]  # x-left, y-left, x-right, y-right
# buttons = [0] * 16           # 16 botones
# last_axes = [0.0]*4
# last_buttons = [0]*16

# # =========================
# # BUCLE PRINCIPAL
# # =========================
# running = True
# while running:
    # # -------------------------
    # # PROCESAR EVENTOS PYGAME
    # # -------------------------
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
            # running = False

    # # -------------------------
    # # TECLADO: ESTADO CONTINUO
    # # -------------------------
    # keys = pygame.key.get_pressed()

    # # Eje X
    # if keys[pygame.K_a]:
        # axes[0] = -1.0
        # print("Tecla presionada: A")
    # elif keys[pygame.K_d]:
        # axes[0] = 1.0
        # print("Tecla presionada: D")
    # else:
        # axes[0] = 0.0

    # # Eje Y
    # if keys[pygame.K_w]:
        # axes[1] = -1.0
        # print("Tecla presionada: W")
    # elif keys[pygame.K_s]:
        # axes[1] = 1.0
        # print("Tecla presionada: S")
    # else:
        # axes[1] = 0.0

    # # Botón A (espacio)
    # buttons[0] = 1 if keys[pygame.K_SPACE] else 0

    # # -------------------------
    # # JOYSTICK (si existe)
    # # -------------------------
    # if joy:
        # # Ejes
        # for i in range(min(4, joy.get_numaxes())):
            # val = joy.get_axis(i)
            # if abs(val) < DEADZONE:
                # val = 0.0
            # axes[i] = val
            # # DEBUG solo si cambió
            # if round(val, 2) != round(last_axes[i], 2):
                # print(f"Eje {i}: {val:.2f}")
                # last_axes[i] = val
        # # Botones
        # for i in range(min(16, joy.get_numbuttons())):
            # val = joy.get_button(i)
            # buttons[i] = val
            # if val != last_buttons[i]:
                # estado = "Presionado" if val else "Liberado"
                # print(f"Botón {i}: {estado}")
                # last_buttons[i] = val

    # # -------------------------
    # # EMPAQUETADO UDP
    # # -------------------------
    # timestamp = time.time()
    # packet = struct.pack("d4f16B", timestamp, axes[0], axes[1], axes[2], axes[3], *buttons)

    # # Enviar al servidor
    # sock.sendto(packet, (SERVER_IP, PORT))

    # # Limitar frecuencia
    # dt = clock.tick(SEND_RATE_HZ)
    # # DEBUG frecuencia de envío
    # # print(f"Tiempo ciclo: {dt} ms")

# # =========================
# # SALIDA LIMPIA
# # =========================
# pygame.quit()
# sys.exit()


import pygame
import socket
import struct
import time
import sys

# =========================
# CONFIGURACIÓN
# =========================
SERVER_IP = '127.0.0.1'  # IP del servidor
PORT = 8081
SEND_RATE_HZ = 250           # Frecuencia de envío UDP
DEADZONE = 0.1               # Zona muerta para joysticks

# =========================
# INICIALIZACIÓN PYGAME
# =========================
pygame.init()
pygame.joystick.init()

# Crear ventana obligatoria para capturar teclado
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Cliente Control - Pygame")

clock = pygame.time.Clock()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# =========================
# DETECCIÓN DE JOYSTICK
# =========================
if pygame.joystick.get_count() > 0:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print("Joystick detectado:", joy.get_name())
else:
    joy = None
    print("No hay joystick, usando teclado solamente")

print("Haz CLICK dentro de la ventana para capturar teclado.")

# =========================
# ESTADO INTERNO
# =========================
axes = [0.0, 0.0, 0.0, 0.0]  # Left stick X/Y, Right stick X/Y
buttons = [0] * 16           # 16 botones
last_axes = [0.0]*4
last_buttons = [0]*16

# =========================
# BUCLE PRINCIPAL
# =========================
running = True
max_loop_time = 0
max_dt = 0
while running:
    #start = time.perf_counter()
    # -------------------------
    # PROCESAR EVENTOS PYGAME
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #print(max_loop_time)
            print(max_dt)
            running = False

    # -------------------------
    # TECLADO: 
    # -------------------------
    keys = pygame.key.get_pressed()

    # Left stick WASD
    if keys[pygame.K_a]:
        axes[0] = -1.0
    elif keys[pygame.K_d]:
        axes[0] = 1.0
    else:
        axes[0] = 0.0

    # Left stick Y
    if keys[pygame.K_w]:
        axes[1] = -1.0
    elif keys[pygame.K_s]:
        axes[1] = 1.0
    else:
        axes[1] = 0.0

    # Right stick: FLECHAS
    if keys[pygame.K_LEFT]:
        axes[2] = -1.0
    elif keys[pygame.K_RIGHT]:
        axes[2] = 1.0
    else:
        axes[2] = 0.0

    if keys[pygame.K_UP]:
        axes[3] = -1.0
    elif keys[pygame.K_DOWN]:
        axes[3] = 1.0
    else:
        axes[3] = 0.0

    # Botón A (ESPACIO)
    buttons[0] = 1 if keys[pygame.K_SPACE] else 0

    # -------------------------
    # JOYSTICK FÍSICO (si existe)
    # -------------------------
    if joy:
        # Ejes
        for i in range(min(4, joy.get_numaxes())):
            val = joy.get_axis(i)
            if abs(val) < DEADZONE:
                val = 0.0
            axes[i] = val
            # DEBUG solo si cambia
            if round(val, 2) != round(last_axes[i], 2):
                print(f"Eje {i}: {val:.2f}")
                last_axes[i] = val
        # Botones
        for i in range(min(16, joy.get_numbuttons())):
            val = joy.get_button(i)
            buttons[i] = val
            if val != last_buttons[i]:
                estado = "Presionado" if val else "Liberado"
                print(f"Botón {i}: {estado}")
                last_buttons[i] = val

    # -------------------------
    # DEBUG: mostrar teclas
    # -------------------------
    pressed_keys = []
    for key, name in [(pygame.K_w, "W"), (pygame.K_a, "A"), (pygame.K_s, "S"), 
                      (pygame.K_d, "D"), (pygame.K_SPACE, "SPACE"),
                      (pygame.K_UP, "UP"), (pygame.K_DOWN, "DOWN"),
                      (pygame.K_LEFT, "LEFT"), (pygame.K_RIGHT, "RIGHT")]:
        if keys[key]:
            pressed_keys.append(name)
    if pressed_keys:
        print("Teclas presionadas:", pressed_keys)

    # -------------------------
    # EMPAQUETADO UDP
    # -------------------------
    timestamp = time.time()
    packet = struct.pack("d4f16B", timestamp, axes[0], axes[1], axes[2], axes[3], *buttons)

    sock.sendto(packet, (SERVER_IP, PORT))

    # Limitar frecuencia
    dt = clock.tick(SEND_RATE_HZ)
    if dt > max_dt:
        max_dt = dt
    #end = time.perf_counter()
    #loop_time = end-start
    #if loop_time>max_loop_time:
    #    max_loop_time = loop_time
    print(max_dt)

# =========================
# SALIDA LIMPIA
# =========================
pygame.quit()
sys.exit()