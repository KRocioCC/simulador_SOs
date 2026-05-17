def fifo(paginas, marcos):
    memoria = []
    fallos  = 0
    for p in paginas:
        if p not in memoria:
            fallos += 1
            if len(memoria) >= marcos:
                memoria.pop(0)
            memoria.append(p)
    return {"fallos": fallos, "aciertos": len(paginas) - fallos, "total": len(paginas)}


def lru(paginas, marcos):
    memoria = []
    fallos  = 0
    for p in paginas:
        if p not in memoria:
            fallos += 1
            if len(memoria) >= marcos:
                memoria.pop(0)
            memoria.append(p)
        else:
            memoria.remove(p)
            memoria.append(p)
    return {"fallos": fallos, "aciertos": len(paginas) - fallos, "total": len(paginas)}


def optimo(paginas, marcos):
    memoria = []
    fallos  = 0
    for i, p in enumerate(paginas):
        if p not in memoria:
            fallos += 1
            if len(memoria) >= marcos:
                usos_futuros = {}
                for m in memoria:
                    try:
                        usos_futuros[m] = paginas[i + 1:].index(m)
                    except ValueError:
                        usos_futuros[m] = float("inf")
                victima = max(usos_futuros, key=usos_futuros.get)
                memoria.remove(victima)
            memoria.append(p)
    return {"fallos": fallos, "aciertos": len(paginas) - fallos, "total": len(paginas)}
