def fcfs_disco(cilindros, cabeza_inicial=50):
    movimientos = 0
    pos   = cabeza_inicial
    orden = []
    for c in cilindros:
        movimientos += abs(c - pos)
        orden.append(c)
        pos = c
    return {"movimientos": movimientos, "orden": orden, "cabeza_inicial": cabeza_inicial}


def sstf(cilindros, cabeza_inicial=50):
    pendientes  = list(cilindros)
    pos         = cabeza_inicial
    movimientos = 0
    orden       = []
    while pendientes:
        cercano      = min(pendientes, key=lambda c: abs(c - pos))
        movimientos += abs(cercano - pos)
        pos          = cercano
        orden.append(cercano)
        pendientes.remove(cercano)
    return {"movimientos": movimientos, "orden": orden, "cabeza_inicial": cabeza_inicial}


def scan(cilindros, cabeza_inicial=50, max_cilindro=199):
    pendientes  = sorted(cilindros)
    pos         = cabeza_inicial
    movimientos = 0
    orden       = []
    derecha   = [c for c in pendientes if c >= pos]
    izquierda = [c for c in pendientes if c < pos][::-1]
    for c in derecha:
        movimientos += abs(c - pos)
        pos = c
        orden.append(c)
    if derecha:
        movimientos += abs(max_cilindro - pos)
        pos = max_cilindro
    for c in izquierda:
        movimientos += abs(c - pos)
        pos = c
        orden.append(c)
    return {"movimientos": movimientos, "orden": orden, "cabeza_inicial": cabeza_inicial}
