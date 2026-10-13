import Pieza

class Rey(Pieza):
    """Se mueve una casilla en cualquier dirección."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2654" if color == "blancas" else "\u265A"
        nombre: str = "Rey blanco" if color == "blancas" else "Rey negro"
        super().__init__(color, simbolo, nombre)