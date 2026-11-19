
from entrega2.modelo.Pieza import Pieza

class Peon(Pieza):
    """Pieza que avanza hacia delante y captura en diagonal."""
    def __init__(self, color: str) -> None:
        simbolo: str = "\u2659" if color == "blancas" else "\u265F"
        nombre: str = "Peón blanco" if color == "blancas" else "Peón negro"
        super().__init__(color, simbolo, nombre)

    def es_movimiento_valido(
        self,
        tablero: Tablero,
        origen: tuple[int, int],
        destino: tuple[int, int],
    ) -> bool:
        """Valida avance simple, doble inicial y captura diagonal según el color."""
        direccion: int = 1 if self.color == "blancas" else -1
        fila_inicial: int = 1 if self.color == "blancas" else 6

        dif_filas: int = destino[0] - origen[0]
        dif_cols: int = abs(destino[1] - origen[1])
        pieza_destino: Pieza | None = tablero.obtener_pieza(destino)

        # 1. Avance recto de 1 casilla
        if dif_cols == 0 and dif_filas == direccion:
            return pieza_destino is None

        # 2. Avance recto de 2 casillas desde fila inicial
        if dif_cols == 0 and dif_filas == 2 * direccion and origen[0] == fila_inicial:
            casilla_intermedia: tuple[int, int] = (origen[0] + direccion, origen[1])
            return (
                tablero.obtener_pieza(casilla_intermedia) is None
                and pieza_destino is None
            )

        # 3. Captura diagonal de 1 casilla
        if dif_cols == 1 and dif_filas == direccion:
            return pieza_destino is not None and pieza_destino.color != self.color

        return False