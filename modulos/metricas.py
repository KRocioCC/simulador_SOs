def metricas_procesador(resultados):
    n = len(resultados)
    return {
        "promedio_espera":  round(sum(r["espera"]  for r in resultados) / n, 2),
        "promedio_retorno": round(sum(r["retorno"] for r in resultados) / n, 2),
        "max_espera":       max(r["espera"] for r in resultados),
        "min_espera":       min(r["espera"] for r in resultados),
    }


def metricas_memoria(resultado):
    total = resultado["total"]
    return {
        "fallos":           resultado["fallos"],
        "aciertos":         resultado["aciertos"],
        "tasa_fallos":      round(resultado["fallos"]   / total * 100, 2),
        "tasa_aciertos":    round(resultado["aciertos"] / total * 100, 2),
    }


def metricas_disco(resultado):
    return {
        "movimientos_totales": resultado["movimientos"],
        "cabeza_inicial":      resultado["cabeza_inicial"],
    }


def metricas_es(resultados):
    n = len(resultados)
    return {
        "promedio_espera":  round(sum(r["espera"]  for r in resultados) / n, 2),
        "promedio_retorno": round(sum(r["retorno"] for r in resultados) / n, 2),
        "max_espera":       max(r["espera"] for r in resultados),
    }
