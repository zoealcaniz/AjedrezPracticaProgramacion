from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dominio.Tablero import Tablero

from dominio.Pieza import Pieza


class Rey(Pieza):
    """Pieza que se mueve una casilla en cualquier dirección."""

    def __init__(self, color: str) -> None:
        """Inicializa un rey con su color, símbolo y nombre."""
        simbolo: str = "\u2654" if color == "blancas" else "\u265A"
        nombre: str = "Rey blanco" if color == "blancas" else "Rey negro"
        super().__init__(color, simbolo, nombre)

    def f_es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """
        Valida desplazamiento de exactamente 1 casilla en fila y/o columna.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el desplazamiento es de 1 casilla como máximo en cada eje,
            False en caso contrario.
        """
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])

        # El rey se mueve como máximo 1 casilla en cualquier dirección
        return dif_filas <= 1 and dif_cols <= 1 and (dif_filas + dif_cols > 0)
