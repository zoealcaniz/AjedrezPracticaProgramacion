import Pieza
from entrega2.modelo import Tablero

class Alfil(Pieza):
    
    """Pieza que se mueve en diagonal cualquier número de casillas."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2657" if color == "blancas" else "\u265D"
        nombre: str = "Alfil blanco" if color == "blancas" else "Alfil negro"
        super().__init__(color, simbolo, nombre)

    def es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """Valida movimiento estrictamente diagonal con camino despejado."""
        dif_filas: int = abs(destino[0] - origen[0])
        dif_cols: int = abs(destino[1] - origen[1])
        if dif_filas != dif_cols or dif_filas == 0:
            return False
        return tablero.camino_libre(origen, destino)