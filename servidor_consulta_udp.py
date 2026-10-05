import socket


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(("0.0.0.0", 5001))

    print("Servidor UDP escuchando en el puerto 5001")

    while True:
        datos, direccion = servidor.recvfrom(1024)
        mensaje = datos.decode("utf-8").strip()

        if mensaje == "ESTADO":
            respuesta = "servidor activo"
        else:
            respuesta = "consulta no reconocida"

        servidor.sendto((respuesta + "\n").encode("utf-8"), direccion)


main()

