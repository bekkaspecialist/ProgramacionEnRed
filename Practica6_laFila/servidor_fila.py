import socket
import threading

PUERTO_TCP = 5050
PUERTO_UDP = 5001

contador_turnos = 0
candado = threading.Lock()


def asignar_turno():
    global contador_turnos

    # Solo un hilo puede incrementar y obtener el turno a la vez.
    with candado:
        contador_turnos += 1
        turno_asignado = contador_turnos

    return turno_asignado

def atender_cliente(conexion, direccion):
    print(f"Cliente conectado: {direccion}")

    with conexion:
        buffer = b""

        while True:
            datos = conexion.recv(1024)

            if not datos:
                break

            # Esperamos mensajes completos antes de interpretarlos.
            buffer += datos

            while b"\n" in buffer:
                linea, buffer = buffer.split(b"\n", 1)
                mensaje = linea.decode("utf-8")

                if mensaje.startswith("TURNO>"):
                    apodo = mensaje.split(">", 1)[1].strip()

                    if apodo:
                        turno = asignar_turno()
                        respuesta = f"turno>{turno}\n"
                        print(f"Turno {turno} asignado a {apodo}")
                    else:
                        respuesta = "error>apodo vacio\n"
                else:
                    respuesta = "error>solicitud no reconocida\n"

                conexion.sendall(respuesta.encode("utf-8"))

    print(f"Conexión cerrada: {direccion}")
def atender_consultas_udp(servidor_udp):
    while True:
        datos, direccion = servidor_udp.recvfrom(1024)
        mensaje = datos.decode("utf-8").strip()

        if mensaje == "CUANTOS":
            # Leemos el contador usando el mismo candado.
            with candado:
                total = contador_turnos

            respuesta = f"van>{total}\n"
        else:
            respuesta = "error>consulta no reconocida\n"

        servidor_udp.sendto(
            respuesta.encode("utf-8"),
            direccion
        )
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_tcp:
        servidor_tcp.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )
        servidor_tcp.bind(("0.0.0.0", PUERTO_TCP))
        servidor_tcp.listen()

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_udp:
            servidor_udp.bind(("0.0.0.0", PUERTO_UDP))

            # UDP espera consultas sin detener la aceptación de clientes TCP.
            hilo_udp = threading.Thread(
                target=atender_consultas_udp,
                args=(servidor_udp,),
                daemon=True
            )
            hilo_udp.start()

            print(f"LA FILA: TCP en {PUERTO_TCP}, UDP en {PUERTO_UDP}")

            while True:
                conexion, direccion = servidor_tcp.accept()

                # Cada cliente tiene su propio hilo de atención.
                hilo_cliente = threading.Thread(
                    target=atender_cliente,
                    args=(conexion, direccion),
                    daemon=True
                )
                hilo_cliente.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor detenido.")

