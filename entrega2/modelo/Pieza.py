from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Tablero import Tablero  # Solo se importa mientras el editor revisa el código, no al ejecutar

class Pieza:
    """Representa una pieza genérica del tablero de ajedrez."""
    def __init__(self, color: str, simbolo: str, nombre: str):
        self.color: str = color
        self.simbolo: str = simbolo
        self.nombre: str = nombre

    def es_movimiento_valido(
        self, tablero: Tablero, origen: tuple[int, int], destino: tuple[int, int]
    ) -> bool:
        """Comprueba si el movimiento cumple las reglas específicas de la pieza."""
        return False