import csv
import io
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Proceso:
    nombre: str
    llegada: int
    rafaga: int


def parsear_procesos(texto: str, limite: int = 10) -> List[Proceso]:
    procesos: List[Proceso] = []
    for linea in texto.strip().splitlines():
        if not linea.strip():
            continue
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) != 3:
            raise ValueError(f"Formato inválido en línea: '{linea}'. Usa nombre,tll,t")
        nombre, llegada, rafaga = partes
        proceso = Proceso(nombre=nombre, llegada=int(llegada), rafaga=int(rafaga))
        if proceso.llegada < 0 or proceso.rafaga <= 0:
            raise ValueError("Los tiempos deben ser: tll >= 0 y t > 0")
        procesos.append(proceso)

    if not procesos:
        raise ValueError("Debes ingresar al menos un proceso")
    if len(procesos) > limite:
        raise ValueError(f"Máximo permitido: {limite} procesos")
    return procesos


def _filas_desde_resultado(resultado: List[Dict]) -> List[Dict]:
    filas: List[Dict] = []
    for item in resultado:
        retorno = item["fin"] - item["llegada"]
        espera = retorno - item["rafaga"]
        penalizacion = round(retorno / item["rafaga"], 2)
        filas.append(
            {
                "proceso": item["id"],
                "tll": item["llegada"],
                "t": item["rafaga"],
                "tini": item["inicio"],
                "tf": item["fin"],
                "T": retorno,
                "E": espera,
                "I": penalizacion,
            }
        )
    return filas


def simular_fcfs(procesos: List[Proceso]) -> Dict:
    procesos_ordenados = sorted(procesos, key=lambda p: (p.llegada, p.nombre))
    tiempo = 0
    filas = []
    gantt = []

    for p in procesos_ordenados:
        inicio = max(tiempo, p.llegada)
        fin = inicio + p.rafaga
        retorno = fin - p.llegada
        espera = retorno - p.rafaga
        penalizacion = round(retorno / p.rafaga, 2)

        filas.append(
            {
                "proceso": p.nombre,
                "tll": p.llegada,
                "t": p.rafaga,
                "tini": inicio,
                "tf": fin,
                "T": retorno,
                "E": espera,
                "I": penalizacion,
            }
        )
        gantt.append({"proceso": p.nombre, "inicio": inicio, "fin": fin, "duracion": p.rafaga})
        tiempo = fin

    return _armar_respuesta("FCFS", filas, gantt)


def simular_sjf(procesos: List[Proceso]) -> Dict:
    pendientes = [{"id": p.nombre, "llegada": p.llegada, "rafaga": p.rafaga} for p in procesos]
    pendientes.sort(key=lambda x: (x["llegada"], x["id"]))
    tiempo = 0
    resultado = []
    gantt = []

    while pendientes:
        disponibles = [p for p in pendientes if p["llegada"] <= tiempo]
        if not disponibles:
            tiempo = pendientes[0]["llegada"]
            continue

        actual = min(disponibles, key=lambda x: (x["rafaga"], x["llegada"], x["id"]))
        pendientes.remove(actual)

        inicio = tiempo
        fin = inicio + actual["rafaga"]
        resultado.append(
            {
                "id": actual["id"],
                "llegada": actual["llegada"],
                "rafaga": actual["rafaga"],
                "inicio": inicio,
                "fin": fin,
            }
        )
        gantt.append(
            {
                "proceso": actual["id"],
                "inicio": inicio,
                "fin": fin,
                "duracion": actual["rafaga"],
            }
        )
        tiempo = fin

    filas = _filas_desde_resultado(resultado)
    return _armar_respuesta("SJF", filas, gantt)


def simular_round_robin(procesos: List[Proceso], quantum: int) -> Dict:
    if quantum <= 0:
        raise ValueError("El quantum debe ser mayor a 0")

    cola = sorted(
        [{"id": p.nombre, "llegada": p.llegada, "rafaga": p.rafaga} for p in procesos],
        key=lambda x: (x["llegada"], x["id"]),
    )

    tiempo = 0
    indice = 0
    queue: List[Dict] = []
    restantes = {p["id"]: p["rafaga"] for p in cola}
    llegadas = {p["id"]: p["llegada"] for p in cola}
    rafagas = {p["id"]: p["rafaga"] for p in cola}
    inicio_real: Dict[str, int] = {}
    fin_real: Dict[str, int] = {}
    gantt: List[Dict] = []

    while queue or indice < len(cola):
        while indice < len(cola) and cola[indice]["llegada"] <= tiempo:
            queue.append(cola[indice])
            indice += 1

        if not queue:
            tiempo = cola[indice]["llegada"]
            continue

        actual = queue.pop(0)
        pid = actual["id"]

        if pid not in inicio_real:
            inicio_real[pid] = tiempo

        ejecutar = min(quantum, restantes[pid])
        inicio = tiempo
        tiempo += ejecutar
        restantes[pid] -= ejecutar

        gantt.append(
            {
                "proceso": pid,
                "inicio": inicio,
                "fin": tiempo,
                "duracion": ejecutar,
            }
        )

        while indice < len(cola) and cola[indice]["llegada"] <= tiempo:
            queue.append(cola[indice])
            indice += 1

        if restantes[pid] > 0:
            queue.append(actual)
        else:
            fin_real[pid] = tiempo

    filas = []
    for p in cola:
        pid = p["id"]
        retorno = fin_real[pid] - llegadas[pid]
        espera = retorno - rafagas[pid]
        filas.append(
            {
                "proceso": pid,
                "tll": llegadas[pid],
                "t": rafagas[pid],
                "tini": inicio_real.get(pid, 0),
                "tf": fin_real[pid],
                "T": retorno,
                "E": espera,
                "I": round(retorno / rafagas[pid], 2),
            }
        )

    filas.sort(key=lambda x: x["tini"])
    return _armar_respuesta(f"Round Robin (q={quantum})", filas, gantt)


def _armar_respuesta(nombre: str, filas: List[Dict], gantt: List[Dict]) -> Dict:
    total_t = sum(f["T"] for f in filas)
    total_e = sum(f["E"] for f in filas)
    n = len(filas)
    tiempo_total = max((seg["fin"] for seg in gantt), default=0)

    return {
        "algoritmo": nombre,
        "filas": filas,
        "gantt": gantt,
        "tiempo_total": tiempo_total,
        "promedio_T": round(total_t / n, 2) if n else 0,
        "promedio_E": round(total_e / n, 2) if n else 0,
        "terminados": [f["proceso"] for f in filas],
        "en_espera_final": [],
    }


def exportar_csv_procesador(filas: List[Dict]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Proceso", "tll", "t", "tini", "tf", "T", "E", "I"])
    for f in filas:
        writer.writerow([f["proceso"], f["tll"], f["t"], f["tini"], f["tf"], f["T"], f["E"], f["I"]])
    return buffer.getvalue()


def parsear_lista_enteros(texto: str) -> List[int]:
    valores = []
    for parte in texto.split(","):
        parte = parte.strip()
        if not parte:
            continue
        numero = int(parte)
        if numero < 0:
            raise ValueError("Solo se permiten enteros no negativos")
        valores.append(numero)
    if not valores:
        raise ValueError("Debes ingresar al menos un valor")
    return valores


def _simular_fcfs_disco(requests: List[int], cabeza: int) -> Tuple[List[int], int]:
    orden = requests[:]
    movimientos = 0
    actual = cabeza
    for r in orden:
        movimientos += abs(r - actual)
        actual = r
    return orden, movimientos


def _simular_scan(requests: List[int], cabeza: int, max_cil: int = 199) -> Tuple[List[int], int]:
    pendientes = sorted(requests)
    derecha = [r for r in pendientes if r >= cabeza]
    izquierda = [r for r in pendientes if r < cabeza][::-1]
    orden = derecha + izquierda

    movimientos = 0
    actual = cabeza
    for r in derecha:
        movimientos += abs(r - actual)
        actual = r
    if derecha:
        movimientos += abs(max_cil - actual)
        actual = max_cil
    for r in izquierda:
        movimientos += abs(r - actual)
        actual = r

    return orden, movimientos


def _simular_cscan(requests: List[int], cabeza: int, max_cil: int = 199) -> Tuple[List[int], int]:
    pendientes = sorted(requests)
    derecha = [r for r in pendientes if r >= cabeza]
    izquierda = [r for r in pendientes if r < cabeza]
    orden = derecha + izquierda

    movimientos = 0
    actual = cabeza
    for r in derecha:
        movimientos += abs(r - actual)
        actual = r
    if izquierda:
        movimientos += abs(max_cil - actual)
        movimientos += max_cil
        actual = 0
    for r in izquierda:
        movimientos += abs(r - actual)
        actual = r

    return orden, movimientos


def _simular_sstf(requests: List[int], cabeza: int) -> Tuple[List[int], int]:
    pendientes = requests[:]
    actual = cabeza
    movimientos = 0
    orden = []
    while pendientes:
        siguiente = min(pendientes, key=lambda x: abs(x - actual))
        movimientos += abs(siguiente - actual)
        actual = siguiente
        orden.append(siguiente)
        pendientes.remove(siguiente)
    return orden, movimientos


def _simular_look(requests: List[int], cabeza: int) -> Tuple[List[int], int]:
    pendientes = sorted(requests)
    derecha = [r for r in pendientes if r >= cabeza]
    izquierda = [r for r in pendientes if r < cabeza][::-1]
    orden = derecha + izquierda
    movimientos = 0
    actual = cabeza
    for r in orden:
        movimientos += abs(r - actual)
        actual = r
    return orden, movimientos


def _simular_clook(requests: List[int], cabeza: int) -> Tuple[List[int], int]:
    pendientes = sorted(requests)
    derecha = [r for r in pendientes if r >= cabeza]
    izquierda = [r for r in pendientes if r < cabeza]
    orden = derecha + izquierda
    movimientos = 0
    actual = cabeza
    for i, r in enumerate(orden):
        if i == len(derecha) and izquierda:
            movimientos += abs(actual - min(izquierda))
            actual = min(izquierda)
        movimientos += abs(r - actual)
        actual = r
    return orden, movimientos


def simular_disco(algoritmo: str, requests: List[int], cabeza: int) -> Dict:
    algoritmo = algoritmo.lower()
    if algoritmo == "fcfs":
        orden, movimientos = _simular_fcfs_disco(requests, cabeza)
    elif algoritmo == "scan":
        orden, movimientos = _simular_scan(requests, cabeza)
    elif algoritmo == "c-scan":
        orden, movimientos = _simular_cscan(requests, cabeza)
    elif algoritmo == "sstf":
        orden, movimientos = _simular_sstf(requests, cabeza)
    elif algoritmo == "look":
        orden, movimientos = _simular_look(requests, cabeza)
    elif algoritmo == "c-look":
        orden, movimientos = _simular_clook(requests, cabeza)
    else:
        raise ValueError("Algoritmo de disco/E-S no soportado")

    puntos = [cabeza] + orden
    pasos = []
    actual = cabeza
    acumulado = 0
    for idx, destino in enumerate(orden, start=1):
        delta = abs(destino - actual)
        acumulado += delta
        pasos.append(
            {
                "paso": idx,
                "desde": actual,
                "hasta": destino,
                "movimiento": delta,
                "acumulado": acumulado,
            }
        )
        actual = destino

    return {
        "algoritmo": algoritmo.upper(),
        "orden": orden,
        "movimientos_totales": movimientos,
        "puntos": puntos,
        "pasos": pasos,
    }


def parsear_memoria(texto: str, limite: int = 10) -> List[Tuple[str, int]]:
    resultado: List[Tuple[str, int]] = []
    for linea in texto.strip().splitlines():
        if not linea.strip():
            continue
        partes = [p.strip() for p in linea.split(",")]
        if len(partes) != 2:
            raise ValueError(f"Formato inválido en línea: '{linea}'. Usa nombre,tamaño")
        nombre, tam = partes
        tam_i = int(tam)
        if tam_i <= 0:
            raise ValueError("El tamaño solicitado debe ser > 0")
        resultado.append((nombre, tam_i))

    if not resultado:
        raise ValueError("Debes ingresar al menos una solicitud")
    if len(resultado) > limite:
        raise ValueError(f"Máximo permitido: {limite} solicitudes")
    return resultado


def simular_memoria(algoritmo: str, solicitudes: List[Tuple[str, int]], particiones: List[int]) -> Dict:
    libres = particiones[:]
    asignaciones = []

    def elegir_indice(req: int) -> int:
        candidatos = [(idx, tam) for idx, tam in enumerate(libres) if tam >= req]
        if not candidatos:
            return -1
        if algoritmo == "first-fit":
            return candidatos[0][0]
        if algoritmo == "best-fit":
            return min(candidatos, key=lambda x: x[1])[0]
        if algoritmo == "worst-fit":
            return max(candidatos, key=lambda x: x[1])[0]
        raise ValueError("Algoritmo de memoria no soportado")

    for nombre, req in solicitudes:
        idx = elegir_indice(req)
        if idx == -1:
            asignaciones.append(
                {
                    "proceso": nombre,
                    "solicitud": req,
                    "particion": "No asignado",
                    "tam_particion": "-",
                    "fragmentacion": "-",
                }
            )
            continue

        tam_part = libres[idx]
        libres[idx] = tam_part - req
        asignaciones.append(
            {
                "proceso": nombre,
                "solicitud": req,
                "particion": f"P{idx + 1}",
                "tam_particion": tam_part,
                "fragmentacion": tam_part - req,
            }
        )

    return {
        "algoritmo": algoritmo,
        "particiones_originales": particiones,
        "particiones_libres_final": libres,
        "asignaciones": asignaciones,
    }
