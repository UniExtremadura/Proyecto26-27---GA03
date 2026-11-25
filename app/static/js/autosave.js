/* US-14 · Guardado automático de formularios con data-autosave="<tramite>". */
(function () {
  "use strict";
  var form = document.querySelector("form[data-autosave]");
  if (!form) { return; }
  var tramite = form.getAttribute("data-autosave");
  var url = "/api/borradores/" + encodeURIComponent(tramite);
  var DEBOUNCE_MS = 1500;
  var version = null;
  var temporizador = null;
  var estado = document.createElement("p");
  estado.setAttribute("role", "status");
  estado.className = "autosave-estado";
  form.insertBefore(estado, form.firstChild);

  function mostrarAviso(texto) { estado.textContent = texto; }

  function leerDatos() {
    var datos = {};
    new FormData(form).forEach(function (valor, nombre) {
      if (datos[nombre] === undefined) { datos[nombre] = valor; }
      else if (Array.isArray(datos[nombre])) { datos[nombre].push(valor); }
      else { datos[nombre] = [datos[nombre], valor]; }
    });
    return datos;
  }

  function aplicarDatos(datos) {
    Object.keys(datos).forEach(function (nombre) {
      var valores = [].concat(datos[nombre]);
      var campos = form.querySelectorAll('[name="' + nombre + '"]');
      campos.forEach(function (campo) {
        if (campo.type === "checkbox" || campo.type === "radio") { campo.checked = valores.indexOf(campo.value) !== -1; }
        else { campo.value = valores[0]; }
      });
    });
  }

  function enviar(datos) {
    return fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ datos: datos, base_version: version })
    }).then(function (r) {
      if (!r.ok) { throw new Error("HTTP " + r.status); }
      return r.json();
    }).then(function (res) { version = res.version; return res; });
  }

  // Reintentos con espera exponencial (1 s, 2 s, 4 s... máx. 30 s); sin duplicados:
  // el servidor trata como idempotente el reintento del mismo contenido.
  var pendiente = null;
  var intentos = 0;
  var reintento = null;

  function guardar(datos) {
    pendiente = datos;
    clearTimeout(reintento);
    return enviar(datos).then(function (res) {
      pendiente = null;
      intentos = 0;
      return res;
    }).catch(function (error) {
      intentos += 1;
      var espera = Math.min(30000, 1000 * Math.pow(2, intentos - 1));
      reintento = setTimeout(sincronizarPendiente, espera);
      throw error;
    });
  }

  function sincronizarPendiente() {
    if (pendiente) {
      guardar(pendiente).then(function () { mostrarAviso("Progreso sincronizado."); }).catch(function () { /* se reintenta */ });
    }
  }

  window.addEventListener("offline", function () {
    mostrarAviso("Sin conexión. Tu progreso está protegido y se guardará al volver la conexión.");
  });
  window.addEventListener("online", function () {
    mostrarAviso("Conexión recuperada. Sincronizando tu progreso…");
    sincronizarPendiente();
  });

  function programarGuardado() {
    clearTimeout(temporizador);
    temporizador = setTimeout(function () {
      guardar(leerDatos()).then(function () { mostrarAviso("Progreso guardado."); })
        .catch(function () { mostrarAviso("No se ha podido guardar todavía."); });
    }, DEBOUNCE_MS);
  }

  function recuperar() {
    fetch(url).then(function (r) { return r.ok ? r.json() : null; }).then(function (borrador) {
      if (!borrador) { return; }
      version = borrador.version;
      aplicarDatos(borrador.datos);
      mostrarAviso("Hemos recuperado tu progreso anterior.");
    }).catch(function () { /* sin conexión: se empieza en blanco */ });
  }

  form.addEventListener("input", programarGuardado);
  form.addEventListener("change", programarGuardado);
  recuperar();
})();
