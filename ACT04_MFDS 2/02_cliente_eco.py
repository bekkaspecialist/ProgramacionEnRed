"""Ejercicio 2: ejecutar en dos terminales simultáneamente."""
import socket
import sys
import time

nombre = sys.argv[1] if len(sys.argv) > 1 else "Fer"

try:
    with socket.create_connection(("127.0.0.1", 5091), timeout=4) as conexion:
        conexion.settimeout(4)
        for mensaje in ("hola", "otro", "adios"):
            conexion.sendall(f"{mensaje}\n".encode("utf-8"))
            respuesta = b""
            while not respuesta.endswith(b"\n"):
                parte = conexion.recv(1024)
                if not parte:
                    raise ConnectionError("Servidor desconectado")
                respuesta += parte
            print(f"{nombre}: {respuesta.decode('utf-8').strip()}", flush=True)
            time.sleep(0.7)
except (OSError, UnicodeError) as error:
    print(f"No se completó la prueba: {error}")
