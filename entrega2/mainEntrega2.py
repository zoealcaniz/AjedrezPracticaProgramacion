"""
Punto de entrada principal del proyecto de ajedrez (Entrega 2).
Ejecutar desde la carpeta entrega2 con: python mainEntrega2.py
"""

from pathlib import Path

from modelo.Tablero import Tablero
from historial import (
    f_guardar_historial,
    f_cargar_historial,
    f_exportar_historial_csv,
)

# Constantes de configuración
TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"
RUTA_PARTIDA: Path = Path("partida.txt")
RUTA_CSV: Path = Path("partida.csv")


def f_validacion_casilla(casilla: str) -> bool:
    """
    Devuelve True si el texto representa una casilla válida del tablero (ej. 'e2').

    Parámetros:
        casilla: cadena de texto a validar.
    Devuelve:
        True si tiene 2 caracteres, una letra de columna válida y un número de fila válido.
    """
    return (
        len(casilla) == 2
        and casilla[0] in LETRAS_VALIDAS
        and casilla[1] in NUMEROS_VALIDOS
    )


def f_conversion_coordenadas(casilla: str) -> tuple[int, int]:
    """
    Convierte una casilla en notación algebraica a coordenadas de matriz.

    Parámetros:
        casilla: cadena en notación algebraica, por ejemplo 'e2'.
    Devuelve:
        Tupla (fila, columna) donde fila 0 corresponde a la fila 8 del tablero.
    """
    columna: int = LETRAS_VALIDAS.index(casilla[0])
    fila: int = TAMANO_TABLERO - int(casilla[1])
    return (fila, columna)


def f_parsear_movimiento(
    entrada: str,
) -> tuple[tuple[int, int], tuple[int, int]] | None:
    """
    Valida que la entrada contenga dos casillas válidas y las convierte a coordenadas.

    Parámetros:
        entrada: cadena introducida por el usuario, ej. 'e2 e4'.
    Devuelve:
        Tupla con las coordenadas de origen y destino, o None si la entrada no es válida.
    """
    partes: list[str] = entrada.strip().lower().split()

    if len(partes) != 2:
        return None

    if not f_validacion_casilla(partes[0]) or not f_validacion_casilla(partes[1]):
        return None

    return (
        f_conversion_coordenadas(partes[0]),
        f_conversion_coordenadas(partes[1]),
    )


def f_cargar_partida_guardada(tablero_actual: Tablero) -> tuple[Tablero, list[str], str] | None:
    """
    Intenta cargar y reproducir la partida guardada en RUTA_PARTIDA.

    Parámetros:
        tablero_actual: tablero vacío recién creado que se usará si no hay partida válida.
    Devuelve:
        Tupla (tablero, historial, estado) si la carga fue correcta, o None si no lo fue.
    """
    movimientos_guardados: list[str] = f_cargar_historial(RUTA_PARTIDA)

    tablero_cargado: Tablero = Tablero()
    turno_carga: str = "blancas"
    archivo_valido: bool = True
    partida_terminada: bool = False

    # Reproducir todos los movimientos del historial para reconstruir el estado
    for indice, movimiento in enumerate(movimientos_guardados):
        coords: tuple[tuple[int, int], tuple[int, int]] | None = (
            f_parsear_movimiento(movimiento)
        )

        if coords is None:
            archivo_valido = False
            break

        origen: tuple[int, int]
        destino: tuple[int, int]
        origen, destino = coords

        motivo: str = tablero_cargado.f_validar_movimiento(origen, destino, turno_carga)

        if motivo != "":
            archivo_valido = False
            break

        tablero_cargado.f_mover_pieza(origen, destino)

        color_rival: str = "negras" if turno_carga == "blancas" else "blancas"

        rival_en_jaque: bool = tablero_cargado.f_esta_en_jaque(color_rival)
        rival_tiene_movs: bool = tablero_cargado.f_tiene_movimientos_validos(color_rival)

        if not rival_tiene_movs:
            partida_terminada = True

            # Si la partida terminó antes del último movimiento, el archivo no es válido
            if indice != len(movimientos_guardados) - 1:
                archivo_valido = False

            break

        turno_carga = color_rival

    if not archivo_valido:
        print("El archivo guardado no es válido. Se empieza una partida nueva.")
        return None

    if partida_terminada:
        print("La partida guardada ya había terminado. Se empieza una nueva.")
        return None

    # Determinar de quién es el turno según la paridad del número de movimientos
    estado_cargado: str = "turno_negras" if len(movimientos_guardados) % 2 == 1 else "turno_blancas"

    print("Partida cargada correctamente.")
    return (tablero_cargado, movimientos_guardados, estado_cargado)


def f_iniciar_partida() -> None:
    """
    Bucle principal del juego con validación de turno, reglas, jaque y fin de partida.

    Gestiona la carga de partidas guardadas, la lectura de movimientos del usuario,
    la validación de cada jugada y la detección de jaque mate o rey ahogado.
    """
    tablero: Tablero = Tablero()
    historial: list[str] = []
    estado: str = "turno_blancas"

    # Si existe una partida guardada, preguntar si se desea continuar
    if RUTA_PARTIDA.exists():
        respuesta: str = input(
            "Existe una partida guardada. ¿Quieres continuarla? (s/n): "
        ).strip().lower()

        if respuesta == "s":
            resultado_carga = f_cargar_partida_guardada(tablero)

            if resultado_carga is not None:
                tablero, historial, estado = resultado_carga

    tablero.f_imprimir_tablero()

    while estado != "fin_partida":
        color_turno: str = "blancas" if estado == "turno_blancas" else "negras"
        color_rival: str = "negras" if color_turno == "blancas" else "blancas"

        print(f"Turno de las {color_turno}")
        entrada: str = input("Movimiento (ej. e2 e4), 'exportar' o 'salir': ").strip().lower()

        if entrada == "salir":
            estado = "fin_partida"
            print("Fin de la partida.")

        elif entrada == "exportar":
            f_exportar_historial_csv(historial, RUTA_CSV)
            print("Historial exportado correctamente.")

        else:
            coords: tuple[tuple[int, int], tuple[int, int]] | None = (
                f_parsear_movimiento(entrada)
            )

            if coords is None:
                print("Formato no válido. Escribe origen y destino, por ejemplo: e2 e4")
            else:
                origen: tuple[int, int]
                destino: tuple[int, int]
                origen, destino = coords

                motivo: str = tablero.f_validar_movimiento(origen, destino, color_turno)

                if motivo != "":
                    print(f"Movimiento rechazado: {motivo}")
                else:
                    tablero.f_mover_pieza(origen, destino)
                    print(f"Movimiento realizado: {entrada.split()[0]} -> {entrada.split()[1]}")

                    # Registrar el movimiento y guardar el estado de la partida
                    historial.append(" ".join(entrada.split()))
                    f_guardar_historial(historial, RUTA_PARTIDA)

                    tablero.f_imprimir_tablero()

                    rival_en_jaque: bool = tablero.f_esta_en_jaque(color_rival)
                    rival_tiene_movs: bool = tablero.f_tiene_movimientos_validos(color_rival)

                    if not rival_tiene_movs:
                        if rival_en_jaque:
                            print(f"Jaque mate. Ganan las {color_turno}.")
                        else:
                            print("Tablas por rey ahogado.")
                        estado = "fin_partida"
                    else:
                        if rival_en_jaque:
                            print(f"Jaque a las {color_rival}.")

                        # Cambiar el turno al jugador rival
                        estado = (
                            "turno_negras"
                            if estado == "turno_blancas"
                            else "turno_blancas"
                        )


if __name__ == "__main__":
    f_iniciar_partida()