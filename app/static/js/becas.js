/* US-03 · Actualiza el estado de la beca cada 10 s sin recargar la página. */
(function () {
  "use strict";
  var elemento = document.getElementById("estado-beca");
  if (!elemento) { return; }
  var url = elemento.getAttribute("data-estado-url");
  if (!url) { return; }
  function actualizar() {
    fetch(url, { headers: { "Accept": "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (datos) {
        if (datos && elemento.textContent !== datos.estado_texto) { elemento.textContent = datos.estado_texto; }
      })
      .catch(function () { /* sin conexión: se mantiene el último estado conocido */ });
  }
  setInterval(actualizar, 10000);
})();
