import socket

HOST = "0.0.0.0"
PUERTO = 5001

# Posiciones donde están los barcos
barcos = ["A1", "A2", "B4", "D3", "E5"]

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PUERTO))
servidor.listen(1)

print("Servidor de Batalla Naval iniciado...")
print("Esperando jugador...")

cliente, direccion = servidor.accept()

print("Jugador conectado desde:", direccion)

cliente.send("Bienvenido a Batalla Naval".encode())

while True:

    ataque = cliente.recv(1024).decode().upper()

    if ataque == "SALIR":
        print("El jugador salió.")
        break

    print("Ataque recibido:", ataque)

    if ataque in barcos:

        barcos.remove(ataque)

        respuesta = "IMPACTO"

        if len(barcos) == 0:
            respuesta = "GANASTE - Todos los barcos fueron destruidos"

    else:
        respuesta = "AGUA"

    cliente.send(respuesta.encode())

    if len(barcos) == 0:
        break

cliente.close()
servidor.close()