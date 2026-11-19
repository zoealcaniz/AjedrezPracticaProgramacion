

from entrega2.modelo.Pieza import Pieza
from entrega2.modelo.Alfil import Alfil
from entrega2.modelo.Caballo import Caballo
from entrega2.modelo.Reina import Reina
from entrega2.modelo.Torre import Torre
from entrega2.modelo.Rey import Rey
from entrega2.modelo.Peon import Peon


class Tablero:
    """Guarda la posición de las piezas y las operaciones sobre el tablero."""

    TAMANO: int = 8

    def __init__(self) -> None:
        self.casillas: list[list[Pieza | None]] = [
            [None for _ in range(self.TAMANO)] for _ in range(self.TAMANO)
        ]
        self.colocar_posicion_inicial()

    def colocar_posicion_inicial(self) -> None:
        """Rellena el tablero con la posición inicial estándar."""
        # Fila 8: Piezas negras (índice 0)
        self.casillas[0] = [
            Torre("negras"),
            Caballo("negras"),
            Alfil("negras"),
            Reina("negras"),
            Rey("negras"),
            Alfil("negras"),
            Caballo("negras"),
            Torre("negras"),
        ]

        # Fila 7: Peones negros (índice 1)
        self.casillas[1] = [Peon("negras") for _ in range(self.TAMANO)]

        # Filas 6 a 3: Vacías (índices 2 a 5)
        for fila in range(2, 6):
            self.casillas[fila] = [None for _ in range(self.TAMANO)]

        # Fila 2: Peones blancos (índice 6)
        self.casillas[6] = [Peon("blancas") for _ in range(self.TAMANO)]

        # Fila 1: Piezas blancas (índice 7)
        self.casillas[7] = [
            Torre("blancas"),
            Caballo("blancas"),
            Alfil("blancas"),
            Reina("blancas"),
            Rey("blancas"),
            Alfil("blancas"),
            Caballo("blancas"),
            Torre("blancas"),
        ]