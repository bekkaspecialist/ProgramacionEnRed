import socket

HOST = "10.30.6.103"
PUERTO = 5001

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PUERTO))

mensaje = cliente.recv(1024).decode()

print(mensaje)

while True:

    ataque = input("Ingresa coordenada de ataque (ejemplo A1): ")

    cliente.send(ataque.encode())

    if ataque.upper() == "SALIR":
        break

    respuesta = cliente.recv(1024).decode()

    print("Servidor:", respuesta)

    if "GANASTE" in respuesta:
        break

cliente.close()