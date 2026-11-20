"""
Punto de entrada principal del proyecto de ajedrez (Entrega 2).
Ejecutar desde la carpeta entrega2 con: python mainEntrega2.py
"""

from modelo.Tablero import Tablero
from historial import (
    guardar_historial,
    cargar_historial,
    exportar_historial_csv
)
import os

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
    """Bucle principal con validación de turno, reglas, jaque y fin de partida."""
    tablero: Tablero = Tablero()
    historial: list[str] = []
    estado: str = "turno_blancas"

    if os.path.exists("partida.txt"):
        respuesta: str = input(
            "Existe una partida guardada. ¿Quieres continuarla? (s/n): "
        ).strip().lower()

        if respuesta == "s":
            movimientos_guardados: list[str] = cargar_historial("partida.txt")

            tablero_cargado: Tablero = Tablero()
            turno_carga: str = "blancas"
            archivo_valido: bool = True
            partida_terminada: bool = False

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

                motivo: str = tablero_cargado.validar_movimiento(
                    origen, destino, turno_carga
                )

                if motivo != "":
                    archivo_valido = False
                    break

                tablero_cargado.mover_pieza(origen, destino)

                color_rival: str = (
                    "negras" if turno_carga == "blancas" else "blancas"
                )

                rival_en_jaque: bool = tablero_cargado.esta_en_jaque(
                    color_rival
                )

                rival_tiene_movs: bool = tablero_cargado.tiene_movimientos_validos(
                    color_rival
                )

                if not rival_tiene_movs:
                    partida_terminada = True

                    if indice != len(movimientos_guardados) - 1:
                        archivo_valido = False

                    break

                turno_carga = color_rival

            if not archivo_valido:
                print("El archivo guardado no es válido. Se empieza una partida nueva.")

            elif partida_terminada:
                print("La partida guardada ya había terminado. Se empieza una nueva.")

            else:
                tablero = tablero_cargado
                historial = movimientos_guardados

                if len(historial) % 2 == 1:
                    estado = "turno_negras"
                else:
                    estado = "turno_blancas"

                print("Partida cargada correctamente.")

    tablero.imprimir_tablero()

    while estado != "fin_partida":
        color_turno: str = "blancas" if estado == "turno_blancas" else "negras"
        color_rival: str = "negras" if color_turno == "blancas" else "blancas"

        print(f"Turno de las {color_turno}")
        entrada: str = input("Movimiento (ej. e2 e4), 'exportar' o 'salir': ").strip().lower()

        if entrada == "salir":
            estado = "fin_partida"
            print("Fin de la partida.")

        elif entrada == "exportar":
            exportar_historial_csv(historial, "partida.csv")
            print("Historial exportado correctamente.")

        else:
            coords: tuple[tuple[int, int], tuple[int, int]] | None = (
                f_parsear_movimiento(entrada)
            )
            if coords is None:
                print(
                    "Formato no válido. Escribe origen y destino, por ejemplo: e2 e4"
                )
            else:
                origen: tuple[int, int]
                destino: tuple[int, int]
                origen, destino = coords
                motivo: str = tablero.validar_movimiento(
                    origen, destino, color_turno
                )

                if motivo != "":
                    print(f"Movimiento rechazado: {motivo}")
                else:
                    tablero.mover_pieza(origen, destino)
                    print(f"Movimiento realizado: {entrada.split()[0]} -> {entrada.split()[1]}")
                    historial.append(" ".join(entrada.split()))
                    guardar_historial(historial, "partida.txt")

                    tablero.imprimir_tablero()

                    rival_en_jaque: bool = tablero.esta_en_jaque(color_rival)
                    rival_tiene_movs: bool = tablero.tiene_movimientos_validos(
                        color_rival
                    )

                    if not rival_tiene_movs:
                        if rival_en_jaque:
                            print(f"Jaque mate. Ganan las {color_turno}.")
                        else:
                            print("Tablas por rey ahogado.")
                        estado = "fin_partida"
                    else:
                        if rival_en_jaque:
                            print(f"Jaque a las {color_rival}.")
                        estado = (
                            "turno_negras"
                            if estado == "turno_blancas"
                            else "turno_blancas"
                        )


if __name__ == "__main__":
    main()