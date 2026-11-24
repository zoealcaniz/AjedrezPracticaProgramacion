"""
Capa de infraestructura: persistencia de la partida en archivos de texto y CSV.
Gestiona la lectura y escritura de partida.txt y la exportación a partida.csv.
"""

import csv
from pathlib import Path


def f_guardar_historial(movimientos: list[str], ruta: Path) -> None:
    """
    Guarda todos los movimientos de la partida en un fichero de texto.

    Parámetros:
        movimientos: lista de cadenas con cada movimiento (ej. 'e2 e4').
        ruta: ruta del archivo donde se guardarán los movimientos.
    """
    # Sobrescribe el archivo con todos los movimientos actuales
    with open(ruta, "w", encoding="utf-8") as archivo:
        for movimiento in movimientos:
            archivo.write(movimiento + "\n")


def f_exportar_historial_csv(movimientos: list[str], ruta: Path) -> None:
    """
    Exporta los movimientos de la partida a un archivo CSV con columnas numeradas.

    Parámetros:
        movimientos: lista de cadenas con cada movimiento (ej. 'e2 e4').
        ruta: ruta del archivo CSV donde se exportará el historial.
    """
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)

        # Cabecera del CSV
        escritor.writerow(["numero", "turno", "origen", "destino"])

        for indice, movimiento in enumerate(movimientos):
            partes: list[str] = movimiento.split()

            # Los índices pares corresponden al turno de blancas, los impares al de negras
            turno: str = "blancas" if indice % 2 == 0 else "negras"

            escritor.writerow([indice + 1, turno, partes[0], partes[1]])


def f_cargar_historial(ruta: Path) -> list[str]:
    """
    Lee los movimientos guardados en un fichero y los devuelve en una lista.

    Parámetros:
        ruta: ruta del archivo de texto con los movimientos guardados.
    Devuelve:
        Lista de cadenas con cada movimiento, o lista vacía si el archivo no existe.
    """
    movimientos: list[str] = []

    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                movimiento: str = linea.strip()

                # Ignorar líneas vacías
                if movimiento != "":
                    movimientos.append(movimiento)

    return movimientos
