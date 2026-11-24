from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dominio.Tablero import Tablero

from dominio.Pieza import Pieza


class Alfil(Pieza):
    """Pieza que se mueve en diagonal cualquier número de casillas."""

    def __init__(self, color: str) -> None:
        """Inicializa un alfil con su color, símbolo y nombre."""
        simbolo: str = "\u2657" if color == "blancas" else "\u265D"
        nombre: str = "Alfil blanco" if color == "blancas" else "Alfil negro"
        super().__init__(color, simbolo, nombre)

    def f_es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """
        Valida movimiento estrictamente diagonal con camino despejado.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el movimiento es diagonal y el camino está libre, False en caso contrario.
        """
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])

        # El movimiento es diagonal si la diferencia en filas y columnas es igual
        if dif_filas != dif_cols or dif_filas == 0:
            return False

        return tablero.f_camino_libre(origen, destino)
