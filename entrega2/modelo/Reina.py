from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

from modelo.Pieza import Pieza

class Reina(Pieza):
    """Pieza que se mueve en línea recta o diagonal cualquier número de casillas."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2655" if color == "blancas" else "\u265B"
        nombre: str = "Reina blanca" if color == "blancas" else "Reina negra"
        super().__init__(color, simbolo, nombre)

    def es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """Valida movimiento recto o diagonal con camino despejado."""
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])
        es_recto: bool = origen[0] == destino[0] or origen[1] == destino[1]
        es_diagonal: bool = dif_filas == dif_cols and dif_filas != 0

        if not (es_recto or es_diagonal):
            return False
        return tablero.camino_libre(origen, destino)