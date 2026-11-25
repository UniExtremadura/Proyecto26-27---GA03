"""US-12 · Interfaz de la app de escritorio (Tkinter).

``tkinter`` se importa dentro de la función para poder importar el módulo sin entorno gráfico.
"""
TITULO = "Campus UNEX"
TAMANO = "420x320"
COLOR_ERROR = "#b00020"
COLOR_OK = "#0b5c3b"


def construir_ventana(on_login=None):
    """Crea la ventana de acceso. ``on_login(usuario, clave)`` debe devolver el texto de bienvenida."""
    import tkinter as tk
    from tkinter import ttk

    raiz = tk.Tk()
    raiz.title(TITULO)
    raiz.geometry(TAMANO)
    marco = ttk.Frame(raiz, padding=16)
    marco.pack(fill="both", expand=True)

    ttk.Label(marco, text="Accede a tu campus", font=("TkDefaultFont", 14, "bold")).pack(anchor="w")
    ttk.Label(marco, text="Usuario").pack(anchor="w", pady=(12, 0))
    usuario = ttk.Entry(marco)
    usuario.pack(fill="x")
    ttk.Label(marco, text="Contraseña").pack(anchor="w", pady=(8, 0))
    clave = ttk.Entry(marco, show="•")
    clave.pack(fill="x")
    mensaje = ttk.Label(marco, text="", foreground=COLOR_ERROR, wraplength=380)
    mensaje.pack(anchor="w", pady=8)

    def pulsar():
        if on_login is None:
            return
        try:
            texto = on_login(usuario.get().strip(), clave.get())
        except Exception as error:  # noqa: BLE001 - se muestra al usuario
            mensaje.config(text=str(error), foreground=COLOR_ERROR)
            return
        mensaje.config(text=texto, foreground=COLOR_OK)

    ttk.Button(marco, text="Entrar", command=pulsar).pack(anchor="e")
    raiz.bind("<Return>", lambda _e: pulsar())
    return raiz
