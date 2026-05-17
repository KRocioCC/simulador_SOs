import os
import matplotlib.pyplot as plt
from tabulate import tabulate

from modulos.generador  import generar_procesos, generar_paginas, generar_cilindros, generar_solicitudes_es
from modulos.procesador import fcfs, sjf, round_robin, prioridad
from modulos.memoria    import fifo, lru, optimo
from modulos.disco      import fcfs_disco, sstf, scan
from modulos.es         import fifo_es, prioridad_es, sjf_es
from modulos.metricas   import metricas_procesador, metricas_memoria, metricas_disco, metricas_es

os.makedirs("graficas",   exist_ok=True)
os.makedirs("resultados", exist_ok=True)

N      = 100
MARCOS = 4
CABEZA = 50
QUANTUM = 4

COLORES = ["#4C8BF5", "#34A853", "#FBBC05", "#EA4335"]

# ── Datos de entrada ────────────────────────────────────────────────────────
procesos    = generar_procesos(N)
paginas     = generar_paginas(N)
cilindros   = generar_cilindros(N)
solicitudes = generar_solicitudes_es(N)

def imprimir_seccion(titulo):
    print("\n" + "=" * 55)
    print(f"  {titulo}")
    print("=" * 55)

def guardar_grafica(nombres, valores, titulo, ylabel, archivo):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(nombres, valores, color=COLORES[:len(nombres)])
    ax.set_title(titulo)
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Algoritmo")
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                str(val), ha="center", va="bottom", fontsize=10)
    plt.tight_layout()
    plt.savefig(f"graficas/{archivo}.png", dpi=150)
    plt.close()
    print(f"  Gráfica guardada en graficas/{archivo}.png")

# ── Procesador ──────────────────────────────────────────────────────────────
imprimir_seccion("PROCESADOR")

alg_proc = {
    "FCFS":        fcfs(procesos),
    "SJF":         sjf(procesos),
    "Round Robin": round_robin(procesos, QUANTUM),
    "Prioridad":   prioridad(procesos),
}

tabla_proc = []
for nombre, res in alg_proc.items():
    m = metricas_procesador(res)
    tabla_proc.append([nombre, m["promedio_espera"], m["promedio_retorno"],
                       m["max_espera"], m["min_espera"]])

print(tabulate(tabla_proc,
               headers=["Algoritmo", "T.Espera prom", "T.Retorno prom",
                        "Max espera", "Min espera"],
               tablefmt="fancy_grid"))

guardar_grafica(
    [r[0] for r in tabla_proc],
    [r[1] for r in tabla_proc],
    "Procesador — Tiempo promedio de espera",
    "Tiempo promedio", "procesador"
)

# ── Memoria ─────────────────────────────────────────────────────────────────
imprimir_seccion("MEMORIA")

alg_mem = {
    "FIFO":   fifo(paginas, MARCOS),
    "LRU":    lru(paginas, MARCOS),
    "Optimo": optimo(paginas, MARCOS),
}

tabla_mem = []
for nombre, res in alg_mem.items():
    m = metricas_memoria(res)
    tabla_mem.append([nombre, m["fallos"], m["aciertos"],
                      m["tasa_fallos"], m["tasa_aciertos"]])

print(tabulate(tabla_mem,
               headers=["Algoritmo", "Fallos", "Aciertos",
                        "Tasa fallos %", "Tasa aciertos %"],
               tablefmt="fancy_grid"))

guardar_grafica(
    [r[0] for r in tabla_mem],
    [r[1] for r in tabla_mem],
    f"Memoria — Fallos de página ({MARCOS} marcos)",
    "Número de fallos", "memoria"
)

# ── Disco ────────────────────────────────────────────────────────────────────
imprimir_seccion("DISCO")

alg_disco = {
    "FCFS": fcfs_disco(cilindros, CABEZA),
    "SSTF": sstf(cilindros, CABEZA),
    "SCAN": scan(cilindros, CABEZA),
}

tabla_disco = []
for nombre, res in alg_disco.items():
    m = metricas_disco(res)
    tabla_disco.append([nombre, m["movimientos_totales"], m["cabeza_inicial"]])

print(tabulate(tabla_disco,
               headers=["Algoritmo", "Movimientos totales", "Cabeza inicial"],
               tablefmt="fancy_grid"))

guardar_grafica(
    [r[0] for r in tabla_disco],
    [r[1] for r in tabla_disco],
    "Disco — Movimientos totales del cabezal",
    "Movimientos", "disco"
)

# ── E/S ──────────────────────────────────────────────────────────────────────
imprimir_seccion("ENTRADA / SALIDA")

alg_es = {
    "FIFO":      fifo_es(solicitudes),
    "Prioridad": prioridad_es(solicitudes),
    "SJF":       sjf_es(solicitudes),
}

tabla_es = []
for nombre, res in alg_es.items():
    m = metricas_es(res)
    tabla_es.append([nombre, m["promedio_espera"], m["promedio_retorno"], m["max_espera"]])

print(tabulate(tabla_es,
               headers=["Algoritmo", "T.Espera prom", "T.Retorno prom", "Max espera"],
               tablefmt="fancy_grid"))

guardar_grafica(
    [r[0] for r in tabla_es],
    [r[1] for r in tabla_es],
    "E/S — Tiempo promedio de espera",
    "Tiempo promedio", "es"
)

# ── Fin ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("  Simulacion completada.")
print("  Revisa las carpetas graficas/ y resultados/")
print("=" * 55 + "\n")
