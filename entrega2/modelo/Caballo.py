from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

from modelo.Pieza import Pieza


class Caballo(Pieza):
    """Pieza que se mueve en forma de 'L' y puede saltar sobre otras piezas."""

    def __init__(self, color: str) -> None:
        """Inicializa un caballo con su color, símbolo y nombre."""
        simbolo: str = "\u2658" if color == "blancas" else "\u265E"
        nombre: str = "Caballo blanco" if color == "blancas" else "Caballo negro"
        super().__init__(color, simbolo, nombre)

    def f_es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """
        Valida desplazamiento de 2 casillas en un eje y 1 en el perpendicular.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el movimiento forma una 'L' válida, False en caso contrario.
        """
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])

        # El caballo se mueve 2 en un eje y 1 en el otro (forma de L)
        return (dif_filas == 2 and dif_cols == 1) or (dif_filas == 1 and dif_cols == 2)
