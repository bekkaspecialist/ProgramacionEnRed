"""Ejercicio 2: eco TCP con contador independiente por cliente."""
import socket
import threading

HOST = "0.0.0.0"
PUERTO = 5091


def atender_cliente(conexion, direccion):
    contador = 0  # Cada hilo mantiene su propio contador.
    buffer = ""
    print(f"Cliente conectado: {direccion}", flush=True)
    try:
        with conexion:
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                buffer += datos.decode("utf-8")
                while "\n" in buffer:
                    mensaje, buffer = buffer.split("\n", 1)
                    contador += 1
                    respuesta = f"{contador}>{mensaje}\n"
                    conexion.sendall(respuesta.encode("utf-8"))
                    print(f"{direccion}: {respuesta.strip()}", flush=True)
    except (ConnectionResetError, BrokenPipeError):
        print(f"Cliente desconectado inesperadamente: {direccion}")
    except UnicodeDecodeError:
        print(f"Datos no válidos en UTF-8 de {direccion}")
    finally:
        print(f"Conexión cerrada: {direccion}", flush=True)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            servidor.bind((HOST, PUERTO))
            servidor.listen()
        except OSError as error:
            print(f"No se pudo iniciar el servidor TCP: {error}")
            return
        print(f"Servidor de eco escuchando en TCP {PUERTO}. Ctrl+C para cerrar.", flush=True)
        try:
            while True:
                conexion, direccion = servidor.accept()
                threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServidor de eco detenido.")


if __name__ == "__main__":
    main()
