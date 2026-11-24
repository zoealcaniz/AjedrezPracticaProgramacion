from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

from modelo.Pieza import Pieza


class Peon(Pieza):
    """Pieza que avanza hacia delante y captura en diagonal."""

    def __init__(self, color: str) -> None:
        """Inicializa un peón con su color, símbolo y nombre."""
        simbolo: str = "\u2659" if color == "blancas" else "\u265F"
        nombre: str = "Peón blanco" if color == "blancas" else "Peón negro"
        super().__init__(color, simbolo, nombre)

    def f_es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """
        Valida avance simple, doble inicial y captura diagonal según el color.

        Parámetros:
            tablero: tablero actual con la posición de las piezas.
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si el movimiento es válido para un peón, False en caso contrario.
        """
        # Las blancas avanzan hacia arriba (índice decrece) y las negras hacia abajo
        direccion: int = -1 if self.color == "blancas" else 1
        fila_inicial: int = 6 if self.color == "blancas" else 1

        dif_filas: int = destino[0] - origen[0]
        dif_cols: int = abs(destino[1] - origen[1])
        pieza_destino: Pieza | None = tablero.f_obtener_pieza(destino)

        # 1. Avance recto de 1 casilla: solo si la casilla destino está vacía
        if dif_cols == 0 and dif_filas == direccion:
            return pieza_destino is None

        # 2. Avance recto de 2 casillas desde la fila inicial
        if dif_cols == 0 and dif_filas == 2 * direccion and origen[0] == fila_inicial:
            casilla_intermedia: tuple[int, int] = (origen[0] + direccion, origen[1])
            return (
                tablero.f_obtener_pieza(casilla_intermedia) is None
                and pieza_destino is None
            )

        # 3. Captura diagonal de 1 casilla: solo si hay una pieza rival en destino
        if dif_cols == 1 and dif_filas == direccion:
            return pieza_destino is not None and pieza_destino.color != self.color

        return False