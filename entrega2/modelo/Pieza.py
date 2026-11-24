from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modelo.Tablero import Tablero

class Pieza:
    """Representa una pieza genérica del tablero de ajedrez y almacena sus características."""

    def __init__(self, color: str, simbolo: str, nombre: str) -> None:
        """Inicializa una pieza con su color, símbolo y nombre."""
        self.color: str = color
        self.simbolo: str = simbolo
        self.nombre: str = nombre

    def f_es_movimiento_valido(
        self, tablero: Tablero, origen: tuple[int, int], destino: tuple[int, int]
    ) -> bool:
        """Comprueba si el movimiento cumple las reglas específicas de la pieza."""
        
        return False