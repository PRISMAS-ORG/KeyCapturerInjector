import time,socket, sys
from pynput.keyboard import Controller, Key
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 5001))
#En el server nokia OBLIGATORIO bind ip local
sock.settimeout(60)

keyboard = Controller()

special_keys = {
        "space": Key.space,
        "backspace": Key.backspace,
        "return": Key.enter,
        "up": Key.up,
        "down": Key.down,
        "left": Key.left,
        "right": Key.right,
        "escape": Key.esc
    }


while True:
    try:
        data,_ = sock.recvfrom(4096)
        sock.settimeout(10)# segundos sin recibir nada, y se puede cerrar
        message = json.loads(data.decode('utf-8'))
        tecla = message["key"]
        if tecla == "escape":
            break
        if message["action"]=="pressed":
            #pulsar en pynput
            print(f"Pulsando {tecla}")
            if tecla in special_keys:
                keyboard.press(special_keys[tecla])
            else:
                keyboard.press(tecla)
        elif message["action"]=="released":
            #soltar en pynput
            print(f"Soltando {tecla}")
            if tecla in special_keys:
                keyboard.release(special_keys[tecla])
            else:
                keyboard.release(tecla)



    except KeyboardInterrupt:
        print("Saliendo")
        sys.exit()

    except (ConnectionResetError,socket.timeout):
        time.sleep(0.1)
        continue