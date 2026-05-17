# Simulador de algoritmos de sistemas operativos

Aplicación web completa en **Flask** para simular algoritmos de sistemas operativos con interfaz interactiva.

## Características

- Pantalla principal con diseño de dos columnas (menú lateral + contenido dinámico).
- Simulador de **Procesador**:
  - FCFS
  - SJF
  - Round Robin (con quantum)
- Simulador de **Memoria**:
  - First Fit
  - Best Fit
  - Worst Fit
- Simulador de **E/S**:
  - FCFS
  - SCAN
  - C-SCAN
- Simulador de **Disco**:
  - SSTF
  - LOOK
  - C-LOOK
- Diagrama de Gantt paso a paso (slider) para algoritmos de procesador.
- Tabla de resultados con columnas: Proceso, tll, t, tini, tf, T, E, I.
- Exportación de resultados a CSV.

## Estructura relevante

- `app.py`: servidor Flask y API REST para simulaciones.
- `modulos/web_algoritmos.py`: lógica de simulación para web.
- `templates/index.html`: vista principal.
- `static/css/styles.css`: estilos de la interfaz.
- `static/js/app.js`: lógica del frontend (menú, peticiones y renderizado).
- `modulos/`: módulos originales del proyecto en consola.

## Requisitos

- Python 3.10+
- pip

## Instalación y ejecución

```zsh
cd /Users/black/Desktop/simulador_so
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python app.py
```

Luego abre:

- `http://127.0.0.1:5000`

## Uso rápido (FCFS)

1. En el menú, selecciona `PROCESADOR -> FCFS`.
2. Ajusta el número de procesos (1 a 10).
3. Ingresa líneas con formato `nombre,tll,t`.
4. Haz clic en `▶️ EJECUTAR SIMULACIÓN`.
5. Usa el slider para ver el Gantt paso a paso.
6. Exporta los resultados con `Exportar a CSV`.

## Notas

- Se mantiene `main.py` para la ejecución en consola del proyecto original.
- La app web corre completamente en Flask (sin frameworks JS externos).
