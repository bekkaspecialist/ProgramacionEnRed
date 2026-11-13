"""Ejercicios 5 y 6: LA FILA TCP/UDP tolerante a fallos y registro de errores."""
import socket
import threading
import time

HOST = "0.0.0.0"
PUERTO_TCP = 5091
PUERTO_UDP = 5001
contador_turnos = 0
candado_turnos = threading.Lock()
candado_log = threading.Lock()
ARCHIVO_LOG = "errores_fila.txt"


def registrar_error(direccion, descripcion):
    marca = time.strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{marca} {direccion} {descripcion}"
    print("ERROR:", linea, flush=True)
    # El candado evita líneas mezcladas entre hilos.
    with candado_log:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea + "\n")


def atender_cliente(conexion, direccion):
    buffer = b""
    try:
        with conexion:
            conexion.settimeout(10)
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    if buffer:
                        registrar_error(direccion, "Conexión cerrada con mensaje incompleto")
                    break
                buffer += datos
                if len(buffer) > 8192:
                    registrar_error(direccion, "Mensaje demasiado largo")
                    break
                while b"\n" in buffer:
                    linea, buffer = buffer.split(b"\n", 1)
                    try:
                        mensaje = linea.decode("utf-8").strip()
                    except UnicodeDecodeError:
                        registrar_error(direccion, "Bytes no válidos UTF-8")
                        conexion.sendall(b"ERROR>UTF8\n")
                        continue
                    if not mensaje.startswith("TURNO>") or not mensaje[6:].strip():
                        registrar_error(direccion, f"Protocolo inválido: {mensaje!r}")
                        conexion.sendall(b"ERROR>PROTOCOLO\n")
                        continue
                    apodo = mensaje[6:].strip()
                    with candado_turnos:
                        global contador_turnos
                        contador_turnos += 1
                        turno = contador_turnos
                    conexion.sendall(f"turno>{turno}\n".encode("utf-8"))
                    print(f"Turno {turno} para {apodo} desde {direccion}", flush=True)
    except (ConnectionResetError, ConnectionAbortedError):
        registrar_error(direccion, "Conexión reiniciada abruptamente")
    except BrokenPipeError:
        registrar_error(direccion, "Error al enviar: conexión cerrada")
    except socket.timeout:
        registrar_error(direccion, "Conexión inactiva: tiempo agotado")
    except OSError as error:
        registrar_error(direccion, f"Error de socket: {error}")
    finally:
        print(f"Conexión finalizada: {direccion}", flush=True)


def atender_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor_udp:
        try:
            servidor_udp.bind((HOST, PUERTO_UDP))
        except OSError as error:
            print(f"No se pudo abrir UDP {PUERTO_UDP}: {error}")
            return
        print(f"UDP escuchando en {PUERTO_UDP}", flush=True)
        while True:
            try:
                datos, direccion = servidor_udp.recvfrom(1024)
                try:
                    mensaje = datos.decode("utf-8").strip()
                except UnicodeDecodeError:
                    registrar_error(direccion, "Datagrama UDP UTF-8 inválido")
                    continue
                if mensaje == "CUANTOS":
                    with candado_turnos:
                        total = contador_turnos
                    servidor_udp.sendto(f"van>{total}\n".encode("utf-8"), direccion)
                else:
                    registrar_error(direccion, f"Consulta UDP inválida: {mensaje!r}")
            except OSError as error:
                registrar_error("UDP", f"Error UDP: {error}")


def main():
    hilo_udp = threading.Thread(target=atender_udp, daemon=True, name="UDP")
    hilo_udp.start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_tcp:
        servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            servidor_tcp.bind((HOST, PUERTO_TCP))
            servidor_tcp.listen()
        except OSError as error:
            print(f"No se pudo abrir TCP {PUERTO_TCP}: {error}")
            return
        print(f"LA FILA escuchando en TCP {PUERTO_TCP}. Ctrl+C para detener.", flush=True)
        try:
            while True:
                conexion, direccion = servidor_tcp.accept()
                threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True).start()
        except KeyboardInterrupt:
            print("\nServidor detenido. Archivo de errores:", ARCHIVO_LOG)


if __name__ == "__main__":
    main()
