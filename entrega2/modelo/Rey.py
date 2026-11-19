from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

from modelo.Pieza import Pieza

class Rey(Pieza):
    """ Pieza que se mueve una casilla en cualquier dirección."""

    def __init__(self, color: str) -> None:
        """Inicializa un rey con su color, símbolo y nombre."""
        simbolo: str = "\u2654" if color == "blancas" else "\u265A"
        nombre: str = "Rey blanco" if color == "blancas" else "Rey negro"
        super().__init__(color, simbolo, nombre)

    def es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """Valida desplazamiento de exactamente 1 casilla en fila y/o columna."""
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])
        return dif_filas <= 1 and dif_cols <= 1 and (dif_filas + dif_cols > 0)