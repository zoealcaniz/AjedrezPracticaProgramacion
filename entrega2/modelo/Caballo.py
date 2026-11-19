from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

from modelo.Pieza import Pieza

class Caballo(Pieza):
    """Pieza que se mueve en forma de 'L' y puede saltar sobre otras piezas."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2658" if color == "blancas" else "\u265E"
        nombre: str = "Caballo blanco" if color == "blancas" else "Caballo negro"
        super().__init__(color, simbolo, nombre)

    def es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """Valida desplazamiento de 2 casillas en un eje y 1 en el perpendicular."""
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])
        return (dif_filas == 2 and dif_cols == 1) or (dif_filas == 1 and dif_cols == 2)
