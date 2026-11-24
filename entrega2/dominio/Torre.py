from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dominio.Tablero import Tablero

from dominio.Pieza import Pieza


class Torre(Pieza):
    """Pieza que se mueve en línea recta por filas o columnas."""

    def __init__(self, color: str) -> None:
        """Inicializa una torre con su color, símbolo y nombre."""
        simbolo: str = "\u2656" if color == "blancas" else "\u265C"
        nombre: str = "Torre blanca" if color == "blancas" else "Torre negra"
        super().__init__(color, simbolo, nombre)

    def f_es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """
        Valida movimiento horizontal o vertical con camino despejado.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el movimiento es recto y el camino está libre, False en caso contrario.
        """
        if origen == destino:
            return False

        # El movimiento es recto solo si comparte fila o columna
        if origen[0] != destino[0] and origen[1] != destino[1]:
            return False

        return tablero.f_camino_libre(origen, destino)
