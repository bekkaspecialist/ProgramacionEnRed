"""Ejercicios 5/6: pruebas de turnos concurrentes y entradas inválidas."""
import socket
import sys
import threading
import struct

HOST, PUERTO = "127.0.0.1", 5091


def enviar(mensaje, nombre):
    try:
        with socket.create_connection((HOST, PUERTO), timeout=4) as cliente:
            cliente.settimeout(4)
            cliente.sendall(mensaje)
            respuesta = cliente.recv(1024)
            print(f"{nombre}: {respuesta.decode('utf-8').strip()}", flush=True)
    except OSError as error:
        print(f"{nombre}: error: {error}")


def dos_clientes():
    barrera = threading.Barrier(2)
    def pedir(nombre):
        barrera.wait()
        enviar(f"TURNO>{nombre}\n".encode("utf-8"), nombre)
    a = threading.Thread(target=pedir, args=("Fer",))
    b = threading.Thread(target=pedir, args=("Compa",))
    a.start()
    b.start()
    a.join()
    b.join()


def reset_abrupto():
    with socket.create_connection((HOST, PUERTO), timeout=4) as conexion:
        conexion.sendall(b"TURNO>sin_saltonueva_linea")
        conexion.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    print("Se provocó una desconexión abrupta (RST).")


modo = sys.argv[1] if len(sys.argv) > 1 else "normal"
if modo == "normal":
    dos_clientes()
elif modo == "basura":
    enviar(b"MENSAJE_MALO\n", "Protocolo inválido")
elif modo == "utf8":
    enviar(b"\xff\xfe\n", "UTF-8 inválido")
elif modo == "rst":
    reset_abrupto()
else:
    print("Usos: python3 05_cliente_pruebas.py [normal|basura|utf8|rst]")
