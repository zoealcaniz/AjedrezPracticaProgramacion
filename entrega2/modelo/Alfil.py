import Pieza

class Alfil(Pieza):
    
    """Se mueve en diagonal cualquier número de casillas."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2657" if color == "blancas" else "\u265D"
        nombre: str = "Alfil blanco" if color == "blancas" else "Alfil negro"
        super().__init__(color, simbolo, nombre)