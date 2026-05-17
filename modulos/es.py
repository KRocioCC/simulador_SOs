def fifo_es(solicitudes):
    tiempo      = 0
    resultados  = []
    for s in sorted(solicitudes, key=lambda x: x["tiempo_llegada"]):
        inicio = max(tiempo, s["tiempo_llegada"])
        fin    = inicio + s["duracion"]
        resultados.append({
            "id":      s["id"],
            "tipo":    s["tipo"],
            "llegada": s["tiempo_llegada"],
            "inicio":  inicio,
            "fin":     fin,
            "espera":  inicio - s["tiempo_llegada"],
            "retorno": fin - s["tiempo_llegada"]
        })
        tiempo = fin
    return resultados


def prioridad_es(solicitudes):
    tiempo      = 0
    pendientes  = sorted(solicitudes, key=lambda x: x["tiempo_llegada"])
    completados = []
    while pendientes:
        disponibles = [s for s in pendientes if s["tiempo_llegada"] <= tiempo]
        if not disponibles:
            tiempo = pendientes[0]["tiempo_llegada"]
            continue
        s = min(disponibles, key=lambda x: x["prioridad"])
        pendientes.remove(s)
        inicio = tiempo
        fin    = inicio + s["duracion"]
        completados.append({
            "id":      s["id"],
            "tipo":    s["tipo"],
            "llegada": s["tiempo_llegada"],
            "inicio":  inicio,
            "fin":     fin,
            "espera":  inicio - s["tiempo_llegada"],
            "retorno": fin - s["tiempo_llegada"]
        })
        tiempo = fin
    return completados


def sjf_es(solicitudes):
    tiempo      = 0
    pendientes  = sorted(solicitudes, key=lambda x: x["tiempo_llegada"])
    completados = []
    while pendientes:
        disponibles = [s for s in pendientes if s["tiempo_llegada"] <= tiempo]
        if not disponibles:
            tiempo = pendientes[0]["tiempo_llegada"]
            continue
        s = min(disponibles, key=lambda x: x["duracion"])
        pendientes.remove(s)
        inicio = tiempo
        fin    = inicio + s["duracion"]
        completados.append({
            "id":      s["id"],
            "tipo":    s["tipo"],
            "llegada": s["tiempo_llegada"],
            "inicio":  inicio,
            "fin":     fin,
            "espera":  inicio - s["tiempo_llegada"],
            "retorno": fin - s["tiempo_llegada"]
        })
        tiempo = fin
    return completados
