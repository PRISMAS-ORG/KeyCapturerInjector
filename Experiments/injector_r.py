import socket
import struct
import pyvjoy  # Para simular mando virtual
import time

# =========================
# CONFIGURACIÓN UDP
# =========================
SERVER_IP = '0.0.0.0'  # Escucha en todas las interfaces
PORT = 8081

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, PORT))
print(f"Servidor escuchando en {SERVER_IP}:{PORT}")

sock.settimeout(10)  # 5000 ms

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

# =========================
# BUCLE PRINCIPAL
# =========================
while True:
    try:
        data, addr = sock.recvfrom(1024)
        timestamp, ax0, ax1, ax2, ax3, *buttons = struct.unpack("d4f16B", data)

        # -------------------------
        # DEBUG: mostrar en tiempo real
        # -------------------------
        print(f"\nPaquete de {addr} - t={timestamp:.3f}")
        print(f"Ejes: {[round(ax0,2), round(ax1,2), round(ax2,2), round(ax3,2)]}")
        print(f"Botones: {buttons}")

        # -------------------------
        # MAPEO A VJOY
        # -------------------------
        # Ejes
        j.set_axis(pyvjoy.HID_USAGE_X, axis_to_vjoy(ax0))  # Left stick X
        j.set_axis(pyvjoy.HID_USAGE_Y, axis_to_vjoy(ax1))  # Left stick Y
        j.set_axis(pyvjoy.HID_USAGE_RX, axis_to_vjoy(ax2)) # Right stick X
        j.set_axis(pyvjoy.HID_USAGE_RY, axis_to_vjoy(ax3)) # Right stick Y

        # Botones (vJoy 1-16)
        for i, b in enumerate(buttons[:16]):
            j.set_button(i+1, b)  # vJoy botones empiezan en 1

    except KeyboardInterrupt:
        print("Saliendo...")
        break
        
    except socket.timeout:
        continue

    except Exception as e:
        print("Error:", e)
        continue