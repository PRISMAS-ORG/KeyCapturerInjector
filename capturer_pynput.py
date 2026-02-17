from pynput import keyboard

def on_press(key):
    try:
        print(f"Tecla presionada: {key.char}")
    except AttributeError:
        print(f"Tecla especial presionada: {key}")

def on_release(key):
    print(f"Tecla soltada: {key}")
    
    # Salir con ESC
    if key == keyboard.Key.esc:
        print("Saliendo...")
        return False

print("Escuchando teclado globalmente... (ESC para salir)")

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()