import socket


def main():
    apodo = input("Escribe tu apodo: ").strip()

    if not apodo:
        print("Debes escribir un apodo.")
        return

    with socket.create_connection(("192.168.1.74", 5050), timeout=5) as conexion:
        mensaje = f"TURNO>{apodo}\n"
        conexion.sendall(mensaje.encode("utf-8"))

        buffer = b""

        # Esperamos la respuesta completa, hasta el salto de línea.
        while b"\n" not in buffer:
            datos = conexion.recv(1024)

            if not datos:
                print("El servidor cerró la conexión sin completar la respuesta.")
                return

            buffer += datos

        respuesta, _ = buffer.split(b"\n", 1)
        print(f"Servidor responde: {respuesta.decode('utf-8')}")


main()
