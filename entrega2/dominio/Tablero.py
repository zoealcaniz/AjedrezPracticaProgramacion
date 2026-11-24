"""
Capa de dominio: tablero de ajedrez con las reglas y operaciones sobre las piezas.
No contiene ninguna lógica de entrada/salida ni acceso a archivos.
"""

from dominio.Pieza import Pieza
from dominio.Alfil import Alfil
from dominio.Caballo import Caballo
from dominio.Dama import Dama
from dominio.Torre import Torre
from dominio.Rey import Rey
from dominio.Peon import Peon


class Tablero:
    """Guarda la posición de las piezas y las operaciones sobre el tablero."""

    TAMANO: int = 8

    def __init__(self) -> None:
        """Inicializa un tablero 8x8 vacío y coloca las piezas iniciales."""
        self.casillas: list[list[Pieza | None]] = [
            [None for _ in range(self.TAMANO)] for _ in range(self.TAMANO)
        ]
        self.f_colocar_posicion_inicial()

    def f_colocar_posicion_inicial(self) -> None:
        """Rellena el tablero con la posición inicial estándar del ajedrez."""
        # Fila 8: Piezas negras (índice 0)
        self.casillas[0] = [
            Torre("negras"),
            Caballo("negras"),
            Alfil("negras"),
            Dama("negras"),
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
            Dama("blancas"),
            Rey("blancas"),
            Alfil("blancas"),
            Caballo("blancas"),
            Torre("blancas"),
        ]

    def f_obtener_pieza(self, pos: tuple[int, int]) -> Pieza | None:
        """
        Devuelve la pieza situada en (fila, col) o None si la casilla está vacía.

        Parámetros:
            pos: coordenadas (fila, columna) de la casilla consultada.
        """
        return self.casillas[pos[0]][pos[1]]

    def f_camino_libre(
        self, origen: tuple[int, int], destino: tuple[int, int]
    ) -> bool:
        """
        Comprueba que no haya piezas entre origen y destino (sin incluir extremos).

        Parámetros:
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        Devuelve:
            True si todas las casillas intermedias están vacías, False en caso contrario.
        """
        # Calcular el paso en cada eje (-1, 0 o +1) según la dirección del movimiento
        paso_fila: int = 0
        if destino[0] > origen[0]:
            paso_fila = 1
        elif destino[0] < origen[0]:
            paso_fila = -1

        paso_col: int = 0
        if destino[1] > origen[1]:
            paso_col = 1
        elif destino[1] < origen[1]:
            paso_col = -1

        fila_actual: int = origen[0] + paso_fila
        col_actual: int = origen[1] + paso_col

        # Avanzar casilla a casilla hasta llegar al destino
        while (fila_actual, col_actual) != destino:
            if self.casillas[fila_actual][col_actual] is not None:
                return False
            fila_actual += paso_fila
            col_actual += paso_col

        return True

    def f_mover_pieza(
        self, origen: tuple[int, int], destino: tuple[int, int]
    ) -> None:
        """
        Aplica un movimiento ya validado y gestiona la coronación automática.

        Parámetros:
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
        """
        pieza: Pieza | None = self.casillas[origen[0]][origen[1]]
        self.casillas[destino[0]][destino[1]] = pieza
        self.casillas[origen[0]][origen[1]] = None

        # Coronación: blancas llegan arriba (índice 0), negras llegan abajo (índice 7)
        if isinstance(pieza, Peon):
            if (pieza.color == "blancas" and destino[0] == 0) or (
                pieza.color == "negras" and destino[0] == 7
            ):
                self.casillas[destino[0]][destino[1]] = Dama(pieza.color)

    def f_buscar_rey(self, color: str) -> tuple[int, int] | None:
        """
        Localiza y devuelve las coordenadas (fila, col) del rey del color indicado.

        Parámetros:
            color: color del rey a buscar ('blancas' o 'negras').
        Devuelve:
            Coordenadas (fila, columna) del rey, o None si no se encuentra.
        """
        for fila in range(self.TAMANO):
            for col in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[fila][col]
                if isinstance(pieza, Rey) and pieza.color == color:
                    return (fila, col)
        return None

    def f_casilla_atacada(
        self, casilla: tuple[int, int], color_atacante: str
    ) -> bool:
        """
        Devuelve True si alguna pieza del color atacante puede llegar a esa casilla.

        Parámetros:
            casilla: coordenadas (fila, columna) de la casilla que se quiere comprobar.
            color_atacante: color de las piezas que podrían atacar ('blancas' o 'negras').
        """
        for fila in range(self.TAMANO):
            for col in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[fila][col]
                if pieza is not None and pieza.color == color_atacante:
                    if pieza.f_es_movimiento_valido(self, (fila, col), casilla):
                        return True
        return False

    def f_esta_en_jaque(self, color: str) -> bool:
        """
        Comprueba si el rey del color indicado está bajo amenaza.

        Parámetros:
            color: color del rey que se quiere comprobar ('blancas' o 'negras').
        Devuelve:
            True si el rey está en jaque, False en caso contrario.
        """
        pos_rey: tuple[int, int] | None = self.f_buscar_rey(color)
        if pos_rey is None:
            return False

        color_rival: str = "negras" if color == "blancas" else "blancas"
        return self.f_casilla_atacada(pos_rey, color_rival)

    def f_deja_rey_en_jaque(
        self, origen: tuple[int, int], destino: tuple[int, int], color: str
    ) -> bool:
        """
        Comprueba si un movimiento deja al rey propio en jaque, simulándolo y restaurando.

        Parámetros:
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
            color: color del jugador que realiza el movimiento.
        Devuelve:
            True si tras el movimiento el rey propio queda en jaque, False en caso contrario.
        """
        pieza_origen: Pieza | None = self.casillas[origen[0]][origen[1]]
        pieza_destino: Pieza | None = self.casillas[destino[0]][destino[1]]

        # Simulación provisional del movimiento
        self.casillas[destino[0]][destino[1]] = pieza_origen
        self.casillas[origen[0]][origen[1]] = None

        en_jaque: bool = self.f_esta_en_jaque(color)

        # Restauración exacta del estado anterior
        self.casillas[origen[0]][origen[1]] = pieza_origen
        self.casillas[destino[0]][destino[1]] = pieza_destino

        return en_jaque

    def f_validar_movimiento(
        self, origen: tuple[int, int], destino: tuple[int, int], turno: str
    ) -> str:
        """
        Valida un movimiento en el orden exigido por las reglas del ajedrez.

        Parámetros:
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
            turno: color del jugador que intenta mover ('blancas' o 'negras').
        Devuelve:
            Cadena vacía '' si el movimiento es válido, o el motivo del rechazo.
        """
        if origen == destino:
            return "El origen y el destino son la misma casilla."

        pieza_origen: Pieza | None = self.f_obtener_pieza(origen)
        if pieza_origen is None:
            return "No hay ninguna pieza en la casilla de origen."

        if pieza_origen.color != turno:
            return f"Esa pieza no es tuya: es el turno de las {turno}."

        pieza_destino: Pieza | None = self.f_obtener_pieza(destino)
        if pieza_destino is not None and pieza_destino.color == turno:
            return "La casilla de destino está ocupada por una pieza propia."

        if isinstance(pieza_destino, Rey):
            return "No se puede capturar al rey contrario."

        if not pieza_origen.f_es_movimiento_valido(self, origen, destino):
            return f"Movimiento no permitido para esta pieza ({pieza_origen.nombre})."

        if self.f_deja_rey_en_jaque(origen, destino, turno):
            return "Ese movimiento deja a tu propio rey en jaque."

        return ""

    def f_tiene_movimientos_validos(self, color: str) -> bool:
        """
        Comprueba si existe al menos un movimiento legal para el color indicado.

        Parámetros:
            color: color del jugador a comprobar ('blancas' o 'negras').
        Devuelve:
            True si hay al menos un movimiento válido disponible, False en caso contrario.
        """
        for fila_orig in range(self.TAMANO):
            for col_orig in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[fila_orig][col_orig]
                if pieza is not None and pieza.color == color:
                    for fila_dest in range(self.TAMANO):
                        for col_dest in range(self.TAMANO):
                            motivo: str = self.f_validar_movimiento(
                                (fila_orig, col_orig), (fila_dest, col_dest), color
                            )
                            if motivo == "":
                                return True
        return False
