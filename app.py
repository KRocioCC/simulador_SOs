from flask import Flask, jsonify, render_template, request, Response

from modulos.web_algoritmos import (
    exportar_csv_procesador,
    parsear_lista_enteros,
    parsear_memoria,
    parsear_procesos,
    simular_disco,
    simular_fcfs,
    simular_memoria,
    simular_round_robin,
    simular_sjf,
)


app = Flask(__name__)


TEMPLATES = {
    "procesador/fcfs": "procesador_fcfs.html",
    "procesador/sjf": "procesador_sjf.html",
    "procesador/round-robin": "procesador_round_robin.html",
    "memoria/first-fit": "memoria_first_fit.html",
    "memoria/best-fit": "memoria_best_fit.html",
    "memoria/worst-fit": "memoria_worst_fit.html",
    "es/fcfs": "es_fcfs.html",
    "es/scan": "es_scan.html",
    "es/c-scan": "es_c_scan.html",
    "disco/sstf": "disco_sstf.html",
    "disco/look": "disco_look.html",
    "disco/c-look": "disco_c_look.html",
}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/vista/<path:clave>")
def vista_parcial(clave: str):
    nombre = TEMPLATES.get(clave)
    if not nombre:
        return jsonify({"error": "Vista no encontrada"}), 404
    return render_template(nombre)


@app.post("/api/simular/procesador/<algoritmo>")
def simular_procesador_api(algoritmo: str):
    try:
        data = request.get_json(force=True)
        procesos = parsear_procesos(data.get("procesos", ""), limite=int(data.get("numero", 10)))

        if algoritmo == "fcfs":
            resultado = simular_fcfs(procesos)
        elif algoritmo == "sjf":
            resultado = simular_sjf(procesos)
        elif algoritmo == "round-robin":
            quantum = int(data.get("quantum", 1))
            resultado = simular_round_robin(procesos, quantum)
        else:
            return jsonify({"error": "Algoritmo de procesador no soportado"}), 400

        return jsonify(resultado)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.post("/api/exportar/csv")
def exportar_csv_api():
    try:
        data = request.get_json(force=True)
        filas = data.get("filas", [])
        contenido = exportar_csv_procesador(filas)
        return Response(
            contenido,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=resultado_simulacion.csv"},
        )
    except Exception:
        return jsonify({"error": "No se pudo generar el CSV"}), 400


@app.post("/api/simular/memoria/<algoritmo>")
def simular_memoria_api(algoritmo: str):
    try:
        data = request.get_json(force=True)
        solicitudes = parsear_memoria(data.get("solicitudes", ""), limite=int(data.get("numero", 10)))
        particiones = parsear_lista_enteros(data.get("particiones", "100,500,200,300,600"))
        resultado = simular_memoria(algoritmo, solicitudes, particiones)
        return jsonify(resultado)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.post("/api/simular/es/<algoritmo>")
def simular_es_api(algoritmo: str):
    try:
        data = request.get_json(force=True)
        solicitudes = parsear_lista_enteros(data.get("solicitudes", "98,183,37,122,14,124,65,67"))
        cabeza = int(data.get("cabeza", 53))
        resultado = simular_disco(algoritmo, solicitudes, cabeza)
        return jsonify(resultado)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


@app.post("/api/simular/disco/<algoritmo>")
def simular_disco_api(algoritmo: str):
    try:
        data = request.get_json(force=True)
        solicitudes = parsear_lista_enteros(data.get("solicitudes", "98,183,37,122,14,124,65,67"))
        cabeza = int(data.get("cabeza", 53))
        resultado = simular_disco(algoritmo, solicitudes, cabeza)
        return jsonify(resultado)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Error interno del servidor"}), 500


if __name__ == "__main__":
    app.run(debug=True)
