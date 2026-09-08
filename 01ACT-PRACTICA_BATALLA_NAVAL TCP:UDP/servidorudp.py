import socket

HOST = "0.0.0.0"
PUERTO = 5002

# Posiciones de los barcos
barcos = ["A1", "A2", "B4", "D3", "E5"]

# Creamos socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Asociamos IP y puerto
servidor.bind((HOST, PUERTO))

print("Servidor UDP de Batalla Naval iniciado...")
print("Esperando ataques...")

while True:

    # Recibe mensaje y dirección del cliente
    datos, direccion_cliente = servidor.recvfrom(1024)

    ataque = datos.decode().upper()

    print("Ataque recibido:", ataque)
    print("Desde:", direccion_cliente)

    if ataque == "SALIR":
        respuesta = "Juego terminado"
        servidor.sendto(respuesta.encode(), direccion_cliente)
        break

    if ataque in barcos:

        barcos.remove(ataque)

        if len(barcos) == 0:
            respuesta = "GANASTE - Todos los barcos fueron destruidos"
        else:
            respuesta = "IMPACTO"

    else:
        respuesta = "AGUA"

    # Envía respuesta al cliente
    servidor.sendto(respuesta.encode(), direccion_cliente)

    if len(barcos) == 0:
        break

servidor.close()