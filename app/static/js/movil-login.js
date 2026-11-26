/* US-13 · Inicio de sesión de la app móvil: obtiene el token y lo guarda solo en la sesión. */
(function () {
  "use strict";
  var form = document.getElementById("form-login");
  if (!form) { return; }
  form.addEventListener("submit", function (evento) {
    evento.preventDefault();
    var error = document.getElementById("error");
    error.textContent = "";
    fetch("/api/token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: form.usuario.value.trim(), password: form.clave.value })
    }).then(function (r) { return r.json().then(function (d) { return { ok: r.ok, datos: d }; }); })
      .then(function (res) {
        if (!res.ok) { error.textContent = res.datos.error || "No se ha podido iniciar sesión."; return; }
        sessionStorage.setItem("token", res.datos.token);
        window.location.href = "/m/";
      })
      .catch(function () { error.textContent = "Sin conexión con el servidor."; });
  });
})();
