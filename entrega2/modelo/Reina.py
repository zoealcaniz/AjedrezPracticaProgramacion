import Pieza

class Reina(Pieza):
    """Se mueve en recta o diagonal cualquier número de casillas."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2655" if color == "blancas" else "\u265B"
        nombre: str = "Reina blanca" if color == "blancas" else "Reina negra"
        super().__init__(color, simbolo, nombre)