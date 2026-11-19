"""
Punto de entrada principal del proyecto de ajedrez (Entrega 2).
Ejecutar desde la carpeta raíz con: python -m entrega2.main
"""

from modelo.Tablero import Tablero

TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"


def f_validacion_casilla(casilla: str) -> bool:
    """Devuelve True si el texto es una casilla válida (ej. 'e2')."""
    return (
        len(casilla) == 2
        and casilla[0] in LETRAS_VALIDAS
        and casilla[1] in NUMEROS_VALIDOS
    )


def f_conversion_coordenadas(casilla: str) -> tuple[int, int]:
    """Convierte 'e2' en (fila, columna) donde fila 0 es la 8 del ajedrez."""
    columna: int = LETRAS_VALIDAS.index(casilla[0])
    fila: int = TAMANO_TABLERO - int(casilla[1])
    return (fila, columna)


def f_parsear_movimiento(
    entrada: str,
) -> tuple[tuple[int, int], tuple[int, int]] | None:
    """Valida que la entrada sean dos casillas válidas ('e2 e4') y las convierte."""
    partes: list[str] = entrada.strip().lower().split()
    if len(partes) != 2:
        return None
    if not f_validacion_casilla(partes[0]) or not f_validacion_casilla(partes[1]):
        return None
    return (
        f_conversion_coordenadas(partes[0]),
        f_conversion_coordenadas(partes[1]),
    )


def main() -> None:
    """Bucle principal de prueba para tablero y movimientos básicos."""
    tablero: Tablero = Tablero()
    tablero.imprimir_tablero()

    estado: str = "turno_blancas"

    while estado != "fin_partida":
        color_turno: str = "blancas" if estado == "turno_blancas" else "negras"
        print(f"Turno de las {color_turno}")
        entrada: str = input("Movimiento (ej. e2 e4) o 'salir': ").strip().lower()

        if entrada == "salir":
            estado = "fin_partida"
            print("Fin de la partida.")
        else:
            coords: tuple[tuple[int, int], tuple[int, int]] | None = (
                f_parsear_movimiento(entrada)
            )
            if coords is None:
                print("Formato no válido. Escribe origen y destino, por ejemplo: e2 e4")
            else:
                tablero.mover_pieza(coords[0], coords[1])
                tablero.imprimir_tablero()
                estado = (
                    "turno_negras" if estado == "turno_blancas" else "turno_blancas"
                )


if __name__ == "__main__":
    main()