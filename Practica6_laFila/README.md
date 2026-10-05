# Práctica 6 — Concurrencia con hilos TCP y UDP

## Programación en Red

Esta práctica tiene como objetivo trabajar con concurrencia mediante hilos en Python y aplicar comunicación de red utilizando los protocolos TCP y UDP.

Durante la práctica se realizaron diferentes ejercicios antes de construir el sistema final **LA FILA**.

## Contenido

### Hilos

`holamundo_hilos.py`

Ejemplo básico de concurrencia utilizando el módulo `threading`.  
Se crean dos hilos que ejecutan una función de manera concurrente y se utiliza `join()` para esperar a que ambos terminen.

### Servidor de eco TCP

`servidor_eco_tcp.py`  
`cliente_eco_tcp.py`

Permiten comprobar la comunicación TCP entre cliente y servidor.

El cliente envía los mensajes:

- hola
- redes
- adios

El servidor devuelve cada mensaje recibido.

También se comprobó que el servidor puede atender varios clientes utilizando un hilo independiente para cada conexión.

### Consulta UDP

`servidor_consulta_udp.py`  
`cliente_consulta_udp.py`

Se utiliza UDP para realizar una consulta sencilla al servidor.

El cliente envía:

`ESTADO`

y el servidor responde:

`servidor activo`

El cliente utiliza un timeout de 3 segundos para evitar esperar indefinidamente si el servidor no responde.

## Sistema de turnos LA FILA

El ejercicio final implementa un sistema sencillo de asignación de turnos.

Archivos:

`servidor_fila.py`  
`cliente_turno_tcp.py`  
`cliente_cuantosudp.py`

### TCP

El cliente solicita un turno enviando su apodo al servidor.

Ejemplo:

`TURNO>bekka specialist`

El servidor responde con un número consecutivo:

`turno>1`

Cada cliente TCP es atendido mediante un hilo independiente.

El contador de turnos se protege mediante `threading.Lock()` para evitar que dos clientes reciban el mismo turno al realizar solicitudes simultáneas.

### UDP

UDP permite consultar cuántos turnos han sido asignados.

El cliente envía:

`CUANTOS`

El servidor responde, por ejemplo:

`van>4`

## Puertos utilizados

- TCP: `5050`
- UDP: `5001`

Se utilizó el puerto TCP 5050 debido a que el puerto 5000 se encontraba ocupado en el equipo servidor.

## Pruebas realizadas

La práctica fue probada entre:

- macOS como servidor
- Debian 12 como cliente

Se comprobó:

- conectividad entre ambos equipos;
- comunicación TCP;
- comunicación UDP;
- atención concurrente de clientes;
- asignación consecutiva de turnos;
- protección del contador compartido;
- consulta del número total de turnos mediante UDP.

En la prueba concurrente se asignaron los turnos 3 y 4 sin repeticiones y posteriormente UDP respondió `van>4`.

## Tecnologías utilizadas

- Python 3
- socket
- threading
- TCP
- UDP
- Debian 12
- macOS
