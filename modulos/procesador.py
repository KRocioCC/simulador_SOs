def fcfs(procesos):
    tiempo = 0
    resultados = []
    for p in sorted(procesos, key=lambda x: x["llegada"]):
        inicio = max(tiempo, p["llegada"])
        fin = inicio + p["rafaga"]
        resultados.append({
            "id": p["id"],
            "llegada": p["llegada"],
            "rafaga": p["rafaga"],
            "inicio": inicio,
            "fin": fin,
            "espera": inicio - p["llegada"],
            "retorno": fin - p["llegada"]
        })
        tiempo = fin
    return resultados


def sjf(procesos):
    tiempo = 0
    pendientes = sorted(procesos, key=lambda x: x["llegada"])
    completados = []
    while pendientes:
        disponibles = [p for p in pendientes if p["llegada"] <= tiempo]
        if not disponibles:
            tiempo = pendientes[0]["llegada"]
            continue
        p = min(disponibles, key=lambda x: x["rafaga"])
        pendientes.remove(p)
        inicio = tiempo
        fin = inicio + p["rafaga"]
        completados.append({
            "id": p["id"],
            "llegada": p["llegada"],
            "rafaga": p["rafaga"],
            "inicio": inicio,
            "fin": fin,
            "espera": inicio - p["llegada"],
            "retorno": fin - p["llegada"]
        })
        tiempo = fin
    return completados


def round_robin(procesos, quantum=4):
    cola = sorted(procesos, key=lambda x: x["llegada"])
    tiempo = 0
    restantes = {p["id"]: p["rafaga"] for p in cola}
    llegadas  = {p["id"]: p["llegada"] for p in cola}
    rafagas   = {p["id"]: p["rafaga"]  for p in cola}
    inicios   = {}
    fines     = {}
    queue     = []
    i         = 0

    while queue or i < len(cola):
        while i < len(cola) and cola[i]["llegada"] <= tiempo:
            queue.append(cola[i])
            i += 1
        if not queue:
            tiempo = cola[i]["llegada"]
            continue
        p   = queue.pop(0)
        pid = p["id"]
        if pid not in inicios:
            inicios[pid] = tiempo
        ejecutar        = min(quantum, restantes[pid])
        restantes[pid] -= ejecutar
        tiempo         += ejecutar
        while i < len(cola) and cola[i]["llegada"] <= tiempo:
            queue.append(cola[i])
            i += 1
        if restantes[pid] > 0:
            queue.append(p)
        else:
            fines[pid] = tiempo

    resultados = []
    for p in cola:
        pid = p["id"]
        resultados.append({
            "id":      pid,
            "llegada": llegadas[pid],
            "rafaga":  rafagas[pid],
            "inicio":  inicios.get(pid, 0),
            "fin":     fines.get(pid, 0),
            "espera":  fines.get(pid, 0) - llegadas[pid] - rafagas[pid],
            "retorno": fines.get(pid, 0) - llegadas[pid]
        })
    return resultados


def prioridad(procesos):
    tiempo    = 0
    pendientes = sorted(procesos, key=lambda x: x["llegada"])
    completados = []
    while pendientes:
        disponibles = [p for p in pendientes if p["llegada"] <= tiempo]
        if not disponibles:
            tiempo = pendientes[0]["llegada"]
            continue
        p = min(disponibles, key=lambda x: x["prioridad"])
        pendientes.remove(p)
        inicio = tiempo
        fin    = inicio + p["rafaga"]
        completados.append({
            "id":      p["id"],
            "llegada": p["llegada"],
            "rafaga":  p["rafaga"],
            "inicio":  inicio,
            "fin":     fin,
            "espera":  inicio - p["llegada"],
            "retorno": fin - p["llegada"]
        })
        tiempo = fin
    return completados
