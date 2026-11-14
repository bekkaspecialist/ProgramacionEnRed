import requests

BASE = "http://localhost:8001"

r = requests.post(
    f"{BASE}/incidencias",
    json={"tipo": "alerta", "descripcion": "Escaneo de puertos"},
    timeout=10
)
print("POST:", r.status_code, r.json())
id_inc = r.json()["id"]

# Consultar con filtros
for filtros in (
    {"tipo": "alerta"},
    {"estado": "abierta"},
    {"tipo": "alerta", "estado": "abierta"},
    {"tipo": "alerta", "estado": "resuelta"},
):
    r = requests.get(f"{BASE}/incidencias", params=filtros, timeout=10)
    print("GET:", filtros, r.status_code, r.json())

# Actualizar
r = requests.patch(
    f"{BASE}/incidencias/{id_inc}",
    json={"estado": "resuelta"},
    timeout=10
)
print("PATCH:", r.status_code, r.json())

# Consultar registro inexistente
r = requests.get(f"{BASE}/incidencias/999", timeout=10)
print("GET inexistente:", r.status_code, r.json())

# Auditoría
print("Contadores:", requests.get(f"{BASE}/contadores", timeout=10).json())
print("Logs:", requests.get(f"{BASE}/logs", timeout=10).json())