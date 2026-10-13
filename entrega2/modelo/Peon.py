
import Pieza


class Peon(Pieza):
    def __init__(self, color: str) -> None:
        simbolo: str = "\u2659" if color == "blancas" else "\u265F"
        nombre: str = "Peón blanco" if color == "blancas" else "Peón negro"
        super().__init__(color, simbolo, nombre)