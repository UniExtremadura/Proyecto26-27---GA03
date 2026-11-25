"""Cliente HTTP de la API del campus (solo biblioteca estándar)."""
import json
import urllib.error
import urllib.request


class ApiError(Exception):
    def __init__(self, mensaje, estado=None):
        super().__init__(mensaje)
        self.estado = estado


class CampusClient:
    def __init__(self, base_url="http://127.0.0.1:5000", abrir=urllib.request.urlopen, timeout=10):
        self.base_url = base_url.rstrip("/")
        self._abrir = abrir          # inyectable para las pruebas
        self.timeout = timeout
        self.token = None

    def _peticion(self, metodo, ruta, datos=None):
        cuerpo = json.dumps(datos).encode("utf-8") if datos is not None else None
        peticion = urllib.request.Request(self.base_url + ruta, data=cuerpo, method=metodo)
        peticion.add_header("Accept", "application/json")
        if cuerpo is not None:
            peticion.add_header("Content-Type", "application/json")
        if self.token:
            peticion.add_header("Authorization", f"Bearer {self.token}")
        try:
            with self._abrir(peticion, timeout=self.timeout) as respuesta:
                return json.loads(respuesta.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            try:
                mensaje = json.loads(error.read().decode("utf-8")).get("error")
            except (ValueError, AttributeError):
                mensaje = None
            raise ApiError(mensaje or f"Error del servidor ({error.code}).", error.code) from error
        except urllib.error.URLError as error:
            raise ApiError("No se puede conectar con el servidor del campus.") from error
