import socket

HOST = "10.30.6.103"
PUERTO = 5002

# Creamos socket UDP
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Batalla Naval - Cliente UDP")
print("Escribe SALIR para terminar.")

while True:

    ataque = input("Ingresa coordenada de ataque (ejemplo A1): ").upper()

    # Envía ataque al servidor
    cliente.sendto(
        ataque.encode(),
        (HOST, PUERTO)
    )

    # Espera respuesta
    datos, direccion_servidor = cliente.recvfrom(1024)

    respuesta = datos.decode()

    print("Servidor:", respuesta)

    if ataque == "SALIR":
        break

    if "GANASTE" in respuesta:
        break

cliente.close()
