import random

def generar_procesos(n=100, semilla=42):
    random.seed(semilla)
    procesos = []
    for i in range(n):
        procesos.append({
            "id": f"P{i+1}",
            "llegada": random.randint(0, 50),
            "rafaga": random.randint(1, 20),
            "prioridad": random.randint(1, 10)
        })
    return sorted(procesos, key=lambda p: p["llegada"])

def generar_paginas(n=100, num_paginas=10, semilla=42):
    random.seed(semilla)
    return [random.randint(0, num_paginas - 1) for _ in range(n)]

def generar_cilindros(n=100, max_cilindro=199, semilla=42):
    random.seed(semilla)
    return [random.randint(0, max_cilindro) for _ in range(n)]

def generar_solicitudes_es(n=100, semilla=42):
    random.seed(semilla)
    tipos = ["lectura", "escritura"]
    solicitudes = []
    for i in range(n):
        solicitudes.append({
            "id": f"S{i+1}",
            "tipo": random.choice(tipos),
            "tiempo_llegada": random.randint(0, 50),
            "duracion": random.randint(1, 15),
            "prioridad": random.randint(1, 10)
        })
    return sorted(solicitudes, key=lambda s: s["tiempo_llegada"])
