/* US-13 · App móvil: carga el resumen con el token de la sesión. */
(function () {
  "use strict";
  var estado = document.getElementById("estado");
  if (!estado) { return; }
  var token = sessionStorage.getItem("token");
  if (!token) { window.location.href = "/m/login"; return; }
  fetch("/api/m/resumen", { headers: { "Authorization": "Bearer " + token } })
    .then(function (r) {
      if (r.status === 401) { sessionStorage.removeItem("token"); window.location.href = "/m/login"; return null; }
      return r.json();
    })
    .then(function (datos) {
      if (!datos) { return; }
      estado.textContent = "Hola, " + datos.usuario + ". Matrículas activas: " + datos.matriculas_activas +
        " (" + datos.creditos + " ECTS).";
    })
    .catch(function () { estado.textContent = "No se puede cargar tu resumen. Comprueba tu conexión."; });
})();
