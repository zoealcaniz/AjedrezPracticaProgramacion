import Pieza

class Torre(Pieza):
    """Se mueve en línea recta por filas o columnas."""
    
    def __init__(self, color: str) -> None:
        simbolo: str = "\u2656" if color == "blancas" else "\u265C"
        nombre: str = "Torre blanca" if color == "blancas" else "Torre negra"
        super().__init__(color, simbolo, nombre)
