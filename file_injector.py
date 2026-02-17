import time
from pynput.keyboard import Controller, Key

# -------- CONFIG --------
FILE_PATH = "texto.txt"
DELAY = 0.5  # segundos entre teclas
# ------------------------

keyboard = Controller()

print("Tienes 5 segundos para poner el foco en el programa destino...")
time.sleep(5)

try:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("Comenzando inyección...")

    for char in content:
        # Manejo básico de saltos de línea
        if char == "\n":
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            keyboard.press(char)
            keyboard.release(char)

        time.sleep(DELAY)

    print("Inyección terminada.")

except FileNotFoundError:
    print("No se encontró el fichero.")