import threading
import time


def saludar(nombre):
    for i in range(3):
        print(f"{nombre}: hola {i}")
        time.sleep(1)


def main():
    hilo_ana = threading.Thread(target=saludar, args=("Ana",))
    hilo_beto = threading.Thread(target=saludar, args=("Beto",))

    hilo_ana.start()
    hilo_beto.start()

    hilo_ana.join()
    hilo_beto.join()

    print("Fin del programa")


main()
