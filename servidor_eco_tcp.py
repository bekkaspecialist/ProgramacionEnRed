import socket
import threading


def atender_cliente(conexion, direccion):
    print(f"Cliente conectado: {direccion}")

    with conexion:
        buffer = b""

        while True:
            datos = conexion.recv(1024)

            if not datos:
                break

            # Acumulamos bytes hasta tener una línea completa.
            buffer += datos

            while b"\n" in buffer:
                linea, buffer = buffer.split(b"\n", 1)
                conexion.sendall(linea + b"\n")

    print(f"Conexión cerrada: {direccion}")


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5050))
    servidor.listen()

    print("Servidor TCP escuchando en el puerto 5050")

    while True:
        conexion, direccion = servidor.accept()

        hilo = threading.Thread(
            target=atender_cliente,
            args=(conexion, direccion),
            daemon=True
        )
        hilo.start()


main()
