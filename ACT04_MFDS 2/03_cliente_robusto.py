"""Ejercicio 3: cliente con mensajes de error y salida distinta de cero."""
import socket
import sys


def recibir_linea(conexion):
    respuesta = b""
    while b"\n" not in respuesta:
        datos = conexion.recv(1024)
        if not datos:
            raise ConnectionError("El servidor se desconectó durante la conversación")
        respuesta += datos
    return respuesta.split(b"\n", 1)[0].decode("utf-8")


def main():
    host = input("IP del servidor [127.0.0.1]: ").strip() or "127.0.0.1"
    try:
        puerto = int(input("Puerto [5091]: ").strip() or "5091")
        if not 1 <= puerto <= 65535:
            raise ValueError
    except ValueError:
        print("ERROR: puerto inválido")
        return 1

    try:
        with socket.create_connection((host, puerto), timeout=3) as conexion:
            conexion.settimeout(3)
            for mensaje in ("hola", "redes", "adios"):
                conexion.sendall(f"{mensaje}\n".encode("utf-8"))
                print(f"Respuesta: {recibir_linea(conexion)}")
        return 0
    except ConnectionRefusedError:
        print("ERROR: el servidor está apagado o rechaza la conexión")
    except socket.gaierror:
        print("ERROR: IP o nombre del servidor no se puede resolver")
    except (socket.timeout, TimeoutError):
        print("ERROR: el servidor no respondió a tiempo")
    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, ConnectionError):
        print("ERROR: el servidor se desconectó a media conversación")
    except UnicodeDecodeError:
        print("ERROR: respuesta con codificación UTF-8 no válida")
    except OSError as error:
        print(f"ERROR: fallo de red ({error})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
