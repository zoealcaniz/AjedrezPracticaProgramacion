import csv
import os
from typing import Any, TextIO

def guardar_historial(movimientos: list[str], ruta: str) -> None:
    """Guarda todos los movimientos de la partida en un fichero."""

    archivo: TextIO = open(ruta, "w", encoding="utf-8")
    for movimiento in movimientos:
        archivo.write(movimiento + "\n")

    archivo.close()

def exportar_historial_csv(movimientos: list[str], ruta: str) -> None:
    """Exporta los movimientos de la partida a un archivo CSV."""

    archivo: TextIO = open(ruta, "w", newline="", encoding="utf-8")
    escritor: Any = csv.writer(archivo)

    escritor.writerow(["numero", "turno", "origen", "destino"])

    for indice, movimiento in enumerate(movimientos):
        partes: list[str] = movimiento.split()

        turno: str = "blancas" if indice % 2 == 0 else "negras"

        escritor.writerow([
            indice + 1,
            turno,
            partes[0],
            partes[1]
        ])

    archivo.close()

def cargar_historial(ruta: str) -> list[str]:
    """Lee los movimientos guardados en un fichero y los devuelve en una lista."""

    movimientos: list[str] = []

    if os.path.exists(ruta):
        archivo: TextIO = open(ruta, "r", encoding="utf-8")

        for linea in archivo:
            movimiento: str = linea.strip()

            if movimiento != "":
                movimientos.append(movimiento)

        archivo.close()

    return movimientos