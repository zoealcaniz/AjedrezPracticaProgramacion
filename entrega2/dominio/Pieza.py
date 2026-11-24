from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dominio.Tablero import Tablero


class Pieza:
    """Representa una pieza genérica del tablero de ajedrez y almacena sus características."""

    def __init__(self, color: str, simbolo: str, nombre: str) -> None:
        """
        Inicializa una pieza con su color, símbolo y nombre.

        Parámetros:
            color: color de la pieza ('blancas' o 'negras').
            simbolo: carácter Unicode que representa la pieza visualmente.
            nombre: nombre descriptivo de la pieza (ej. 'Torre blanca').
        """
        self.color: str = color
        self.simbolo: str = simbolo
        self.nombre: str = nombre

    def f_es_movimiento_valido(
        self, tablero: Tablero, origen: tuple[int, int], destino: tuple[int, int]
    ) -> bool:
        """
        Comprueba si el movimiento cumple las reglas específicas de la pieza.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el movimiento es válido, False en caso contrario.
            La clase base siempre devuelve False; cada pieza sobreescribe este método.
        """
        return False
