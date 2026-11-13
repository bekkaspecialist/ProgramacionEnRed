"""Ejercicio 1: tres hilos con nombres y numero de saludos."""
import threading
import time


def saludar(nombre, veces):
    for n in range(1, veces + 1):
        print(f"{nombre}: saludo {n}/{veces}", flush=True)
        time.sleep(0.15)


personas = [("bekka", 3), ("gallo", 5), ("pato", 2)]
hilos = []

for nombre, veces in personas:
    hilo = threading.Thread(target=saludar, args=(nombre, veces), name=nombre)
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

print("Todos los hilos terminaron. Fin del programa.")
