import time,socket, sys, struct
from pynput.keyboard import Controller, Key
import json
import pyvjoy  # Para simular mando virtual

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8082))
#En el server nokia OBLIGATORIO bind ip local
sock.settimeout(60)

'''
provisional packet
w,a,s,d,e,r,q,up,down,left,right,space,enter,shift_l,ctrl_l,esc
ejes mando: axes[0], axes[1], axes[2], axes[3]
16 botones
'''
packet_format = ">16B4f16B"
teclas_list = ["w","a","s","d","e","r","q","up","down","left","right"\
,"space","return","left shift","left ctrl","escape"]

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

#Preparamos el joystick
# =========================
# INICIALIZAR MANDO VIRTUAL
# =========================
j = pyvjoy.VJoyDevice(1)  # Mando virtual 1
print("Mando virtual listo")

# =========================
# FUNCIONES AUXILIARES
# =========================
def axis_to_vjoy(value):
    """Convierte eje [-1,1] a rango 0-32768 de vJoy"""
    return int((value + 1) / 2 * 32768)

print("Inyector iniciado")
while True:
    try:
        data,_ = sock.recvfrom(48)
        sock.settimeout(10)# segundos sin recibir nada, y se puede cerrar
        #leemos el paquete
        message = struct.unpack(packet_format,data)
        teclas = message[:16]
        ejes = message[16:20]
        buttons = message[20:]
        print(f"Teclas: {teclas}")
        print(f"Ejes: {ejes}")
        print(f"Botones: {buttons}")
        
        for index,tecla_pressed in enumerate(teclas):
            if tecla_pressed == 1:
                #pulsar
                tecla = teclas_list[index]
                if tecla in special_keys:
                    keyboard.press(special_keys[tecla])
                else:
                    keyboard.press(tecla)
            else:
                #soltar
                tecla = teclas_list[index]
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
        j.set_axis(pyvjoy.HID_USAGE_RX, axis_to_vjoy(message[18])) # Right stick X
        j.set_axis(pyvjoy.HID_USAGE_RY, axis_to_vjoy(message[19])) # Right stick Y

        # Botones (vJoy 1-16)
        for i, b in enumerate(message[20:]):
            j.set_button(i+1, b)  # vJoy botones empiezan en 1
        




    except KeyboardInterrupt:
        print("Saliendo")
        sys.exit()

    except Exception as e:#(ConnectionResetError,socket.timeout):
        #time.sleep(0.1)
        print(f"Error {e}")
        continue