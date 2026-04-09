import time,socket, sys, struct
from pynput.keyboard import Controller, Key
from pynput.mouse import Button, Controller as MouseController
import json
import pyvjoy  # Para simular mando virtual
import ctypes 
# Constante de Windows para inyectar movimiento relativo de ratón 
MOUSEEVENTF_MOVE = 0x0001

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8082))
#En el server nokia OBLIGATORIO bind ip local
sock.settimeout(120)

INJECT_KEYS = True
INJECT_GAMEPAD = True
INJECT_MOUSE = True

'''
provisional packet
w,a,s,d,e,r,q,up,down,left,right,space,enter,shift_l,ctrl_l,esc
ejes mando: axes[0], axes[1], axes[2], axes[3]
16 botones
dpad o pov (flechas direccion del mando): dos bytes
3 botones raton: 3 bytes
2 int para movimiento relativo (son 4 bytes cada uno con signo, a veces da -1)
4s, 4 caracteres que informan del estado
tam: 73Bytes
'''
packet_format = ">16B6f16B2b3B2i4s"
packet_len = 73 #bytes
teclas_list = ["w","a","s","d","e","r","q","up","down","left","right"\
,"space","return","left shift","left ctrl","escape"]

#Contrlar el estado real de los switches
teclas_state = [0] * 16 
button_state = [0] * 16
dpad_state = [0] * 2
mouse_button_state = [0] * 3

keyboard = Controller()

special_keys = {
        "space": Key.space,
        "backspace": Key.backspace,
        "return": Key.enter,
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right,
        "escape": Key.esc,
        "left shift":Key.shift,
        "left ctrl":Key.ctrl_l
    }

mouse = MouseController()
mouse.position = (200,200)
old_position_x = 0
old_position_y = 0 

#Preparamos el joystick
j = pyvjoy.VJoyDevice(1)  # Mando virtual 1
print("Mando virtual listo")

def axis_to_vjoy(value):
    """Convierte eje [-1,1] a rango 0-32768 de vJoy"""
    return int((value + 1) / 2 * 32768)

def hat_to_pov(x, y):
    if (x, y) == (0, 0):
        return -1  # centro

    mapping = {
        (0, 1): 0,
        (1, 1): 4500,
        (1, 0): 9000,
        (1, -1): 13500,
        (0, -1): 18000,
        (-1, -1): 22500,
        (-1, 0): 27000,
        (-1, 1): 31500,
    }

    return mapping.get((x, y), -1)

def hat_to_pov_4dir(x, y):
    if x == 0 and y == 0:
        return -1

    if y == 1:
        return 0      # Norte
    if x == 1:
        return 1      # Este
    if y == -1:
        return 2      # Sur
    if x == -1:
        return 3      # Oeste

    return -1

print("Inyector iniciado")

while True:
    try:
        data,_ = sock.recvfrom(packet_len)
        sock.settimeout(60)# segundos sin recibir nada, y se puede cerrar
        #leemos el paquete
        message = struct.unpack(packet_format,data)
        teclas = message[:16]
        ejes = message[16:22]
        buttons = message[22:38]
        dpad = message[38:40]
        mouse_buttons = message[40:43]
        mouse_pos = message[43:45]
        packet_info = message[45].decode().strip('\x00') #si mide menos puede haber byte nulo
        if packet_info != "0000":
            print(f"[State_info]: {packet_info}")
            if packet_info == "exit":
                break
        #print(f"Teclas: {teclas}\nEjes: {ejes}\nBotones: {buttons}\nDpad: {dpad}\nRaton: {mouse_buttons}\nRaton_pos: {mouse_pos}", end="\r")
        #print(f"dpad: {dpad}")
        
        for index,tecla_pressed in enumerate(teclas):
            if tecla_pressed != teclas_state[index]: #Si cambia el estado de la tecla
                tecla = teclas_list[index]
                if tecla_pressed == 1:
                    teclas_state[index] = 1
                    #pulsar
                    if tecla in special_keys:
                        keyboard.press(special_keys[tecla])
                    else:
                        keyboard.press(tecla)
                else:
                    #soltar
                    teclas_state[index] = 0
                    if tecla in special_keys:
                        keyboard.release(special_keys[tecla])
                    else:
                        keyboard.release(tecla)
        #inyectamos el mando
         # -------------------------
        # MAPEO A VJOY
        # -------------------------
        # Ejes
        j.set_axis(pyvjoy.HID_USAGE_X, axis_to_vjoy(message[16]))  # Left stick X
        j.set_axis(pyvjoy.HID_USAGE_Y, axis_to_vjoy(message[17]))  # Left stick Y
        j.set_axis(pyvjoy.HID_USAGE_Z, axis_to_vjoy(message[18]))  # Left stick Z
        j.set_axis(pyvjoy.HID_USAGE_RX, axis_to_vjoy(message[19])) # Right stick X
        j.set_axis(pyvjoy.HID_USAGE_RY, axis_to_vjoy(message[20])) # Right stick Y
        j.set_axis(pyvjoy.HID_USAGE_RZ, axis_to_vjoy(message[21])) # Right stick Z

        # Botones (vJoy 1-16)
        for index, button_value in enumerate(message[22:38]):
            if button_value != button_state[index]:
                j.set_button(index+1, button_value)  # vJoy botones empiezan en 1
                button_state[index] = button_value
        #hat o dpad
        if dpad_state[0] != message[38] or dpad_state[1] != message[39]:
            #pov_value = hat_to_pov(message[38],message[39])
            pov_value = hat_to_pov_4dir(message[38],message[39])
            #print(message[38],message[39],pov_value)
            j.set_disc_pov(1, pov_value)
            dpad_state[0] = message[38]
            dpad_state[1] = message[39]

        #inyeccion de raton
        if message[40] != mouse_button_state[0]:
            #print(f"Mouse left: {message[40]}")
            mouse.press(Button.left) if bool(message[40]) else mouse.release(Button.left)
            mouse_button_state[0] = message[40]
        if message[41] != mouse_button_state[1]:
            mouse.press(Button.middle) if bool(message[41]) else mouse.release(Button.middle)
            mouse_button_state[1] = message[41]
        if message[42] != mouse_button_state[2]:
            mouse.press(Button.right) if bool(message[42]) else mouse.release(Button.right)
            mouse_button_state[2] = message[42]
        #Movimiento moderno
        #mouse.move(message[43],message[44])
        #Movimiento de raton legacy de windows
        if message[43] != 0 or message[44] != 0:
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, message[43], message[44], 0, 0)

    except KeyboardInterrupt:
        print("Saliendo")
        sys.exit()

    except Exception as e:#(ConnectionResetError,socket.timeout):
        #time.sleep(0.1)
        print(f"\nError {e}")
        opcion = input("Pulsa y para salir o n para continuar: ")
        if opcion=="y":
            sys.exit()
        elif opcion=="n":
            continue
        else:
            print("Opcion no reconocida, continuando")
            continue