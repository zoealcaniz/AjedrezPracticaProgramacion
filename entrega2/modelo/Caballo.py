import Pieza

class Caballo(Pieza):
    
    """Se mueve en forma de 'L' y puede saltar sobre otras piezas."""

    def __init__(self, color: str) -> None:
        simbolo: str = "\u2658" if color == "blancas" else "\u265E"
        nombre: str = "Caballo blanco" if color == "blancas" else "Caballo negro"
        super().__init__(color, simbolo, nombre)
