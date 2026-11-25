"""Punto de entrada: python -m desktop.app [URL]"""
import sys

from .client import CampusClient
from .ui import construir_ventana


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    cliente = CampusClient(argv[0] if argv else "http://127.0.0.1:5000")
    construir_ventana(on_login=None).mainloop()
    return cliente


if __name__ == "__main__":
    main()
