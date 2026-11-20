import csv
from typing import TextIO

def guardar_historial(movimientos: list[str], ruta: str) -> None:
    """Guarda todos los movimientos de la partida en un fichero."""

    archivo = open(ruta, "w", encoding="utf-8")

    for movimiento in movimientos:
        archivo.write(movimiento + "\n")

    archivo.close()

def exportar_historial_csv(movimientos: list[str], ruta: str) -> None:
    """Exporta los movimientos de la partida a un archivo CSV."""

    archivo: TextIO = open(ruta, "w", newline="", encoding="utf-8")
    escritor = csv.writer(archivo)

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