from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

from modelo.Pieza import Pieza

class Torre(Pieza):
    """Pieza que se mueve en línea recta por filas o columnas."""
    
    def __init__(self, color: str) -> None:
        """Inicializa una torre con su color, símbolo y nombre."""
        simbolo: str = "\u2656" if color == "blancas" else "\u265C"
        nombre: str = "Torre blanca" if color == "blancas" else "Torre negra"
        super().__init__(color, simbolo, nombre)

    def es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """Valida movimiento horizontal o vertical con camino despejado."""
        if origen == destino:
            return False
        if origen[0] != destino[0] and origen[1] != destino[1]:
            return False
        return tablero.camino_libre(origen, destino)
