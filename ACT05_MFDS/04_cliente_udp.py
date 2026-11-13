"""Ejercicio 4: consultar CUANTOS por UDP, tres intentos y pausas 1, 2 y 4 s."""
import socket
import time

HOST, PUERTO = "127.0.0.1", 5001


def consultar():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(1.5)
        for intento in range(1, 4):
            print(f"Intento {intento}/3: enviando CUANTOS...", flush=True)
            try:
                cliente.sendto(b"CUANTOS", (HOST, PUERTO))
                datos, _ = cliente.recvfrom(1024)
                respuesta = datos.decode("utf-8").strip()
                print(f"Respuesta del servidor: {respuesta}", flush=True)
                return respuesta
            except socket.timeout:
                pausa = 2 ** (intento - 1)
                print(f"Sin respuesta. Esperando {pausa} segundo(s).", flush=True)
                time.sleep(pausa)
            except (OSError, UnicodeDecodeError) as error:
                print(f"Error en consulta: {error}")
                return None
    return None


if __name__ == "__main__":
    if consultar() is None:
        print("No fue posible consultar al servidor tras tres intentos.")
