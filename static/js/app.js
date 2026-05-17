const MENU = {
  PROCESADOR: [
    { id: 'procesador/fcfs', label: 'FCFS (First Come, First Served)' },
    { id: 'procesador/sjf', label: 'SJF (Shortest Job First)' },
    { id: 'procesador/round-robin', label: 'Round Robin' },
  ],
  MEMORIA: [
    { id: 'memoria/first-fit', label: 'First Fit' },
    { id: 'memoria/best-fit', label: 'Best Fit' },
    { id: 'memoria/worst-fit', label: 'Worst Fit' },
  ],
  'E/S': [
    { id: 'es/fcfs', label: 'FCFS (Disk Scheduling)' },
    { id: 'es/scan', label: 'SCAN' },
    { id: 'es/c-scan', label: 'C-SCAN' },
  ],
  DISCO: [
    { id: 'disco/sstf', label: 'SSTF' },
    { id: 'disco/look', label: 'LOOK' },
    { id: 'disco/c-look', label: 'C-LOOK' },
  ],
};

const COLORES = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899'];

const estado = {
  vista: 'procesador/fcfs',
  resultadoProcesador: null,
};

const menuLateral = document.getElementById('menu-lateral');
const vistaPrincipal = document.getElementById('vista-principal');
const mensajeError = document.getElementById('mensaje-error');

function colorPorProceso(nombre) {
  const idx = Math.abs([...nombre].reduce((acc, ch) => acc + ch.charCodeAt(0), 0)) % COLORES.length;
  return COLORES[idx];
}

function mostrarError(msg) {
  mensajeError.textContent = msg;
  mensajeError.className = 'alerta';
}

function limpiarError() {
  mensajeError.textContent = '';
  mensajeError.className = 'oculto';
}

function construirMenu() {
  menuLateral.innerHTML = '';

  Object.entries(MENU).forEach(([seccion, opciones]) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'menu-seccion';

    const titulo = document.createElement('button');
    titulo.className = 'menu-titulo';
    titulo.textContent = seccion;

    const lista = document.createElement('div');
    lista.className = 'menu-opciones';

    opciones.forEach((op) => {
      const btn = document.createElement('button');
      btn.textContent = op.label;
      btn.dataset.vista = op.id;
      if (estado.vista === op.id) btn.classList.add('activo');
      btn.addEventListener('click', () => {
        estado.vista = op.id;
        construirMenu();
        renderVista();
      });
      lista.appendChild(btn);
    });

    titulo.addEventListener('click', () => {
      lista.classList.toggle('oculto');
    });

    wrapper.appendChild(titulo);
    wrapper.appendChild(lista);
    menuLateral.appendChild(wrapper);
  });
}

function renderVista() {
  limpiarError();

  if (estado.vista.startsWith('procesador/')) {
    renderProcesador();
    return;
  }

  if (estado.vista.startsWith('memoria/')) {
    renderMemoria();
    return;
  }

  renderDiscoEs();
}

function renderProcesador() {
  const tpl = document.getElementById('tpl-procesador-fcfs');
  vistaPrincipal.innerHTML = '';
  vistaPrincipal.appendChild(tpl.content.cloneNode(true));

  const [_, algoritmo] = estado.vista.split('/');
  const titulo = vistaPrincipal.querySelector('h2');
  const bloqueRR = vistaPrincipal.querySelector('#bloque-rr');

  if (algoritmo === 'sjf') {
    titulo.textContent = 'Algoritmo de planificación de procesos: SJF (Shortest Job First)';
  }
  if (algoritmo === 'round-robin') {
    titulo.textContent = 'Algoritmo de planificación de procesos: Round Robin';
    bloqueRR.classList.remove('oculto');
  }

  const numeroEl = vistaPrincipal.querySelector('#numero-procesos');
  const textoEl = vistaPrincipal.querySelector('#texto-procesos');
  const quantumEl = vistaPrincipal.querySelector('#quantum');
  const btnEjemplo = vistaPrincipal.querySelector('#btn-ejemplo');
  const btnEjecutar = vistaPrincipal.querySelector('#btn-ejecutar');
  const btnExportar = vistaPrincipal.querySelector('#btn-exportar');
  const ganttWrap = vistaPrincipal.querySelector('#gantt-wrap');
  const tablaWrap = vistaPrincipal.querySelector('#tabla-wrap');
  const pasoContenedor = vistaPrincipal.querySelector('#paso-contenedor');
  const slider = vistaPrincipal.querySelector('#slider-pasos');
  const valorPaso = vistaPrincipal.querySelector('#valor-paso');

  btnEjemplo.addEventListener('click', () => {
    textoEl.value = `A,0,3\nB,0,6\nC,0,4\nD,0,5\nE,0,2`;
    numeroEl.value = 5;
    if (quantumEl) quantumEl.value = 2;
  });

  btnEjecutar.addEventListener('click', async () => {
    try {
      limpiarError();
      const payload = {
        numero: Number(numeroEl.value),
        procesos: textoEl.value,
      };
      if (algoritmo === 'round-robin') payload.quantum = Number(quantumEl.value || 1);

      const resp = await fetch(`/api/simular/procesador/${algoritmo}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await resp.json();
      if (!resp.ok) throw new Error(data.error || 'No se pudo simular');

      estado.resultadoProcesador = data;
      btnExportar.disabled = false;

      slider.min = 1;
      slider.max = data.gantt.length || 1;
      slider.value = slider.max;
      valorPaso.textContent = slider.value;
      pasoContenedor.classList.remove('oculto');

      pintarGantt(data.gantt, Number(slider.value), ganttWrap);
      pintarTablaProcesador(data, tablaWrap);
    } catch (err) {
      mostrarError(err.message);
    }
  });

  slider.addEventListener('input', () => {
    valorPaso.textContent = slider.value;
    if (!estado.resultadoProcesador) return;
    pintarGantt(estado.resultadoProcesador.gantt, Number(slider.value), ganttWrap);
  });

  btnExportar.addEventListener('click', async () => {
    try {
      if (!estado.resultadoProcesador) return;
      const resp = await fetch('/api/exportar/csv', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filas: estado.resultadoProcesador.filas }),
      });
      if (!resp.ok) throw new Error('No se pudo exportar CSV');
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `simulacion_${algoritmo}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      mostrarError(err.message);
    }
  });
}

function pintarGantt(segmentos, pasoActual, contenedor) {
  const visibles = segmentos.slice(0, pasoActual);
  const total = Math.max(...segmentos.map((s) => s.fin), 1);

  const barra = visibles
    .map((seg) => {
      const width = (seg.duracion / total) * 100;
      return `<div class="gantt-segmento" style="width:${width}%; background:${colorPorProceso(seg.proceso)}">${seg.proceso}</div>`;
    })
    .join('');

  const marcas = [0, ...visibles.map((s) => s.fin)]
    .map((t) => `<span>${t}</span>`)
    .join('');

  contenedor.innerHTML = `
    <div class="gantt">
      <h3>Diagrama de Gantt</h3>
      <div class="gantt-barra">${barra}</div>
      <div class="gantt-tiempos">${marcas}</div>
    </div>
  `;
}

function pintarTablaProcesador(data, contenedor) {
  const filas = data.filas
    .map(
      (f) => `<tr>
        <td>${f.proceso}</td>
        <td>${f.tll}</td>
        <td>${f.t}</td>
        <td>${f.tini}</td>
        <td>${f.tf}</td>
        <td>${f.T}</td>
        <td>${f.E}</td>
        <td>${Number(f.I).toFixed(2)}</td>
      </tr>`
    )
    .join('');

  contenedor.innerHTML = `
    <div class="tabla-scroll">
      <table>
        <thead>
          <tr>
            <th>Proceso</th>
            <th>tll (tiempo llegada)</th>
            <th>t (ráfaga)</th>
            <th>tini (inicio)</th>
            <th>tf (fin)</th>
            <th>T (retorno)</th>
            <th>E (espera)</th>
            <th>I (penalización)</th>
          </tr>
        </thead>
        <tbody>${filas}</tbody>
      </table>
    </div>
    <div class="resumen-final">
      <div><b>Promedio de T (retorno):</b> ${data.promedio_T}</div>
      <div><b>Promedio de E (espera):</b> ${data.promedio_E}</div>
      <div><b>Procesos terminados:</b> ${data.terminados.join(', ')}</div>
      <div><b>Procesos en espera al final:</b> ${data.en_espera_final.length ? data.en_espera_final.join(', ') : 'Ninguno'}</div>
    </div>
  `;
}

function renderMemoria() {
  const [_, algoritmo] = estado.vista.split('/');
  vistaPrincipal.innerHTML = `
    <h2>Asignación de memoria: ${algoritmo.toUpperCase()}</h2>
    <p class="resumen">Simulación visual de particiones con tabla de asignación y fragmentación interna.</p>
    <div class="panel-entrada">
      <div class="campo">
        <label>Número de procesos / peticiones</label>
        <input id="mem-num" type="number" min="1" max="10" value="5" />
      </div>
      <div class="campo">
        <label>Procesos (formato: nombre,tamaño)</label>
        <textarea id="mem-sol" rows="7">P1,212\nP2,417\nP3,112\nP4,426\nP5,95</textarea>
      </div>
    </div>
    <div class="campo rr-campo">
      <label>Particiones (coma separada)</label>
      <input id="mem-part" type="text" value="100,500,200,300,600" />
    </div>
    <div class="acciones">
      <button id="mem-run" class="primario">▶️ EJECUTAR SIMULACIÓN</button>
    </div>
    <div id="mem-out"></div>
  `;

  document.getElementById('mem-run').addEventListener('click', async () => {
    try {
      limpiarError();
      const resp = await fetch(`/api/simular/memoria/${algoritmo}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          numero: Number(document.getElementById('mem-num').value),
          solicitudes: document.getElementById('mem-sol').value,
          particiones: document.getElementById('mem-part').value,
        }),
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data.error || 'Error de simulación');

      document.getElementById('mem-out').innerHTML = `
        <div class="tabla-scroll">
          <table>
            <thead>
              <tr><th>Proceso</th><th>Solicitud</th><th>Partición</th><th>Tamaño partición</th><th>Fragmentación</th></tr>
            </thead>
            <tbody>
              ${data.asignaciones
                .map(
                  (a) => `<tr><td>${a.proceso}</td><td>${a.solicitud}</td><td>${a.particion}</td><td>${a.tam_particion}</td><td>${a.fragmentacion}</td></tr>`
                )
                .join('')}
            </tbody>
          </table>
        </div>
        <div class="resumen-final">
          <div><b>Particiones originales:</b> ${data.particiones_originales.join(', ')}</div>
          <div><b>Particiones libres finales:</b> ${data.particiones_libres_final.join(', ')}</div>
        </div>
      `;
    } catch (err) {
      mostrarError(err.message);
    }
  });
}

function renderDiscoEs() {
  const [categoria, algoritmo] = estado.vista.split('/');
  const titulo = categoria === 'es' ? 'E/S' : 'DISCO';

  vistaPrincipal.innerHTML = `
    <h2>${titulo}: ${algoritmo.toUpperCase()}</h2>
    <p class="resumen">Simulación de recorrido del cabezal con tabla de movimientos acumulados.</p>
    <div class="panel-entrada">
      <div class="campo">
        <label>Cabeza inicial</label>
        <input id="d-head" type="number" min="0" value="53" />
      </div>
      <div class="campo">
        <label>Solicitudes de cilindros (coma separada)</label>
        <input id="d-req" type="text" value="98,183,37,122,14,124,65,67" />
      </div>
    </div>
    <div class="acciones">
      <button id="d-run" class="primario">▶️ EJECUTAR SIMULACIÓN</button>
    </div>
    <div id="d-out"></div>
  `;

  document.getElementById('d-run').addEventListener('click', async () => {
    try {
      limpiarError();
      const resp = await fetch(`/api/simular/${categoria}/${algoritmo}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cabeza: Number(document.getElementById('d-head').value),
          solicitudes: document.getElementById('d-req').value,
        }),
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data.error || 'Error de simulación');

      document.getElementById('d-out').innerHTML = `
        <div class="resumen-final">
          <div><b>Orden de atención:</b> ${data.orden.join(' → ')}</div>
          <div><b>Movimientos totales:</b> ${data.movimientos_totales}</div>
        </div>
        <div class="tabla-scroll">
          <table>
            <thead>
              <tr><th>Paso</th><th>Desde</th><th>Hasta</th><th>Movimiento</th><th>Acumulado</th></tr>
            </thead>
            <tbody>
              ${data.pasos
                .map(
                  (p) => `<tr><td>${p.paso}</td><td>${p.desde}</td><td>${p.hasta}</td><td>${p.movimiento}</td><td>${p.acumulado}</td></tr>`
                )
                .join('')}
            </tbody>
          </table>
        </div>
      `;
    } catch (err) {
      mostrarError(err.message);
    }
  });
}

construirMenu();
renderVista();
