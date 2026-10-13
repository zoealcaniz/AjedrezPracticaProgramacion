import Tablero

class Pieza:
    def __init__(self, color: str, simbolo: str, nombre: str):
        self.color: str = color
        self.simbolo: str = simbolo
        self.nombre: str = nombre



    def es_movimiento_valido(
        self, tablero: Tablero, origen: tuple[int, int], destino: tuple[int, int]
    ) -> bool:
        """Comprueba si el movimiento cumple las reglas específicas de la pieza.
        
        Las subclases redefinirán este método con sus propias reglas.
        """
        return False