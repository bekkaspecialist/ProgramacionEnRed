import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(3)

        cliente.sendto(
            "CUANTOS".encode("utf-8"),
            ("192.168.1.74", 5001)
        )

        try:
            datos, direccion = cliente.recvfrom(1024)
            respuesta = datos.decode("utf-8").strip()
            print(f"Servidor responde: {respuesta}")
        except TimeoutError:
            print("No llegó una respuesta en 3 segundos.")


main()
