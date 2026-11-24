from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dominio.Tablero import Tablero

from dominio.Pieza import Pieza


class Dama(Pieza):
    """Pieza que se mueve en línea recta o diagonal cualquier número de casillas."""

    def __init__(self, color: str) -> None:
        """Inicializa una dama con su color, símbolo y nombre."""
        simbolo: str = "\u2655" if color == "blancas" else "\u265B"
        nombre: str = "Dama blanca" if color == "blancas" else "Dama negra"
        super().__init__(color, simbolo, nombre)

    def f_es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """
        Valida movimiento recto o diagonal con camino despejado.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el movimiento es recto o diagonal y el camino está libre,
            False en caso contrario.
        """
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])

        # Movimiento recto: comparte fila o columna con la casilla de destino
        es_recto: bool = origen[0] == destino[0] or origen[1] == destino[1]

        # Movimiento diagonal: diferencia igual en filas y columnas
        es_diagonal: bool = dif_filas == dif_cols and dif_filas != 0

        if not (es_recto or es_diagonal):
            return False

        return tablero.f_camino_libre(origen, destino)
