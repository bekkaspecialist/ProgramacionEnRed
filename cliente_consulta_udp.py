import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(3)

        cliente.sendto(
            "ESTADO\n".encode("utf-8"),
            ("127.0.0.1", 5001)
        )

        try:
            datos, direccion = cliente.recvfrom(1024)
            print(f"Servidor responde: {datos.decode('utf-8').strip()}")
        except TimeoutError:
            print("No llegó una respuesta en 3 segundos.")


main()
