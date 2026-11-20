from modelo.Pieza import Pieza
from modelo.Alfil import Alfil
from modelo.Caballo import Caballo
from modelo.Dama import Dama
from modelo.Torre import Torre
from modelo.Rey import Rey
from modelo.Peon import Peon


class Tablero:
    """Guarda la posición de las piezas y las operaciones sobre el tablero."""

    TAMANO: int = 8
    LETRAS_VALIDAS: str = "abcdefgh"

    def __init__(self) -> None:
        """Inicializa un tablero 8x8 vacío y coloca las piezas iniciales."""
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

    def imprimir_tablero(self) -> None:
        """Imprime el tablero por consola con coordenadas a-h y 1-8 (fila 8 arriba)."""
        encabezado: str = " "
        for indice_columna in range(self.TAMANO):
            letra_columna: str = self.LETRAS_VALIDAS[indice_columna]
            encabezado = encabezado + " " + letra_columna + " "
        print(encabezado)

        for indice_fila in range(self.TAMANO):
            numero_fila: int = self.TAMANO - indice_fila
            linea: str = str(numero_fila)
            for indice_columna in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[indice_fila][indice_columna]
                if pieza is None:
                    celda: str = " . "
                else:
                    celda = " " + pieza.simbolo + " "
                linea = linea + celda
            print(linea)

    def obtener_pieza(self, pos: tuple[int, int]) -> Pieza | None:
        """Devuelve la pieza situada en (fila, col) o None si la casilla está vacía."""
        return self.casillas[pos[0]][pos[1]]

    def camino_libre(self, origen: tuple[int, int], destino: tuple[int, int]) -> bool:
        """Comprueba que no haya piezas entre origen y destino (sin incluir extremos)."""
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

        while (fila_actual, col_actual) != destino:
            if self.casillas[fila_actual][col_actual] is not None:
                return False
            fila_actual += paso_fila
            col_actual += paso_col

        return True

    def mover_pieza(self, origen: tuple[int, int], destino: tuple[int, int]) -> None:
        """Aplica un movimiento ya validado y gestiona la coronación automática."""
        pieza: Pieza | None = self.casillas[origen[0]][origen[1]]
        self.casillas[destino[0]][destino[1]] = pieza
        self.casillas[origen[0]][origen[1]] = None

        # Coronación: blancas llegan arriba (índice 0), negras llegan abajo (índice 7)
        if isinstance(pieza, Peon):
            if (pieza.color == "blancas" and destino[0] == 0) or (
                pieza.color == "negras" and destino[0] == 7
            ):
                self.casillas[destino[0]][destino[1]] = Dama(pieza.color)

    def buscar_rey(self, color: str) -> tuple[int, int] | None:
        """Localiza y devuelve las coordenadas (fila, col) del rey del color indicado."""
        for fila in range(self.TAMANO):
            for col in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[fila][col]
                if isinstance(pieza, Rey) and pieza.color == color:
                    return (fila, col)
        return None

    def casilla_atacada(self, casilla: tuple[int, int], color_atacante: str) -> bool:
        """Devuelve True si alguna pieza del color atacante puede llegar a esa casilla."""
        for fila in range(self.TAMANO):
            for col in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[fila][col]
                if pieza is not None and pieza.color == color_atacante:
                    if pieza.es_movimiento_valido(self, (fila, col), casilla):
                        return True
        return False

    def esta_en_jaque(self, color: str) -> bool:
        """Comprueba si el rey del color indicado está bajo amenaza."""
        pos_rey: tuple[int, int] | None = self.buscar_rey(color)
        if pos_rey is None:
            return False
        color_rival: str = "negras" if color == "blancas" else "blancas"
        return self.casilla_atacada(pos_rey, color_rival)

    def deja_rey_en_jaque(
        self, origen: tuple[int, int], destino: tuple[int, int], color: str
    ) -> bool:
        """Comprueba si un movimiento deja al rey propio en jaque, simulándolo y restaurando el tablero."""        
        pieza_origen: Pieza | None = self.casillas[origen[0]][origen[1]]
        pieza_destino: Pieza | None = self.casillas[destino[0]][destino[1]]

        # Simulación provisional
        self.casillas[destino[0]][destino[1]] = pieza_origen
        self.casillas[origen[0]][origen[1]] = None

        en_jaque: bool = self.esta_en_jaque(color)

        # Restauración exacta
        self.casillas[origen[0]][origen[1]] = pieza_origen
        self.casillas[destino[0]][destino[1]] = pieza_destino

        return en_jaque

    def validar_movimiento(
        self, origen: tuple[int, int], destino: tuple[int, int], turno: str
    ) -> str:
        """Valida un movimiento en el orden exigido. Devuelve '' si es válido o el motivo."""
        if origen == destino:
            return "El origen y el destino son la misma casilla."

        pieza_origen: Pieza | None = self.obtener_pieza(origen)
        if pieza_origen is None:
            return "No hay ninguna pieza en la casilla de origen."

        if pieza_origen.color != turno:
            return f"Esa pieza no es tuya: es el turno de las {turno}."

        pieza_destino: Pieza | None = self.obtener_pieza(destino)
        if pieza_destino is not None and pieza_destino.color == turno:
            return "La casilla de destino está ocupada por una pieza propia."

        if isinstance(pieza_destino, Rey):
            return "No se puede capturar al rey contrario."

        if not pieza_origen.es_movimiento_valido(self, origen, destino):
            return f"Movimiento no permitido para esta pieza ({pieza_origen.nombre})."

        if self.deja_rey_en_jaque(origen, destino, turno):
            return "Ese movimiento deja a tu propio rey en jaque."

        return ""

    def tiene_movimientos_validos(self, color: str) -> bool:
        """Comprueba si existe al menos un movimiento legal para el color indicado."""
        for fila_orig in range(self.TAMANO):
            for col_orig in range(self.TAMANO):
                pieza: Pieza | None = self.casillas[fila_orig][col_orig]
                if pieza is not None and pieza.color == color:
                    for fila_dest in range(self.TAMANO):
                        for col_dest in range(self.TAMANO):
                            motivo: str = self.validar_movimiento(
                                (fila_orig, col_orig), (fila_dest, col_dest), color
                            )
                            if motivo == "":
                                return True
        return False