"""
Capa de aplicación: coordina el desarrollo de la partida de ajedrez.
No contiene ninguna lógica de entrada/salida ni acceso directo a archivos.
"""

from dataclasses import dataclass

from dominio.Tablero import Tablero


# ---------------------------------------------------------------------------
# Constantes para convertir la notación algebraica a coordenadas de matriz
# ---------------------------------------------------------------------------

TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"


# ---------------------------------------------------------------------------
# Dataclasses de resultado (agrupan datos relacionados de forma clara)
# ---------------------------------------------------------------------------

@dataclass
class ResultadoMovimiento:
    """Resultado devuelto tras intentar realizar un movimiento."""

    exito: bool
    motivo: str = ""
    jaque: bool = False
    jaque_mate: bool = False
    tablas: bool = False
    ganador: str | None = None


@dataclass
class ResultadoCarga:
    """Resultado devuelto tras intentar cargar una partida guardada."""

    exito: bool
    # "invalido" si el archivo tiene movimientos incorrectos,
    # "terminada" si la partida ya había concluido
    razon_fallo: str = ""


# ---------------------------------------------------------------------------
# Funciones auxiliares de parseo de notación algebraica
# ---------------------------------------------------------------------------

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
        entrada: cadena con el movimiento, ej. 'e2 e4'.
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


# ---------------------------------------------------------------------------
# Servicio de partida
# ---------------------------------------------------------------------------

class PartidaService:
    """
    Coordina el estado y el desarrollo de una partida de ajedrez completa.

    Gestiona los turnos, el historial de movimientos, la validación delegando
    al dominio y la detección de fin de partida. No realiza ninguna operación
    de entrada/salida ni acceso a archivos.
    """

    def __init__(self) -> None:
        """Inicializa el servicio con un tablero nuevo y el turno de las blancas."""
        self._tablero: Tablero = Tablero()
        self._historial: list[str] = []
        self._turno: str = "blancas"
        self._terminada: bool = False

    def f_obtener_tablero(self) -> Tablero:
        """Devuelve el tablero actual de la partida."""
        return self._tablero

    def f_obtener_historial(self) -> list[str]:
        """Devuelve la lista de movimientos realizados en notación algebraica."""
        return self._historial

    def f_obtener_turno(self) -> str:
        """Devuelve el color del jugador al que le corresponde mover ('blancas' o 'negras')."""
        return self._turno

    def f_esta_terminada(self) -> bool:
        """Devuelve True si la partida ha concluido."""
        return self._terminada

    def f_realizar_movimiento(
        self,
        origen: tuple[int, int],
        destino: tuple[int, int],
        notacion: str,
    ) -> ResultadoMovimiento:
        """
        Valida y ejecuta un movimiento, actualiza el historial y el turno.

        Parámetros:
            origen: coordenadas (fila, columna) de la casilla de origen.
            destino: coordenadas (fila, columna) de la casilla de destino.
            notacion: cadena en notación algebraica (ej. 'e2 e4') para el historial.
        Devuelve:
            ResultadoMovimiento con el resultado del intento de movimiento.
        """
        # Validar el movimiento según las reglas del dominio
        motivo: str = self._tablero.f_validar_movimiento(origen, destino, self._turno)
        if motivo != "":
            return ResultadoMovimiento(exito=False, motivo=motivo)

        # Aplicar el movimiento y registrarlo en el historial
        self._tablero.f_mover_pieza(origen, destino)
        self._historial.append(notacion)

        color_rival: str = "negras" if self._turno == "blancas" else "blancas"
        rival_en_jaque: bool = self._tablero.f_esta_en_jaque(color_rival)
        rival_tiene_movs: bool = self._tablero.f_tiene_movimientos_validos(color_rival)

        resultado: ResultadoMovimiento = ResultadoMovimiento(
            exito=True, jaque=rival_en_jaque
        )

        # Comprobar si la partida ha terminado por jaque mate o rey ahogado
        if not rival_tiene_movs:
            self._terminada = True
            if rival_en_jaque:
                resultado.jaque_mate = True
                resultado.ganador = self._turno
            else:
                resultado.tablas = True
        else:
            # Cambiar el turno al jugador rival
            self._turno = color_rival

        return resultado

    def f_cargar_desde_movimientos(
        self, movimientos: list[str]
    ) -> ResultadoCarga:
        """
        Reproduce una lista de movimientos para restaurar el estado de la partida.

        Si la carga es correcta, actualiza el tablero, el historial y el turno internos.

        Parámetros:
            movimientos: lista de cadenas en notación algebraica.
        Devuelve:
            ResultadoCarga indicando si la carga fue correcta o el motivo del fallo.
        """
        tablero_temporal: Tablero = Tablero()
        turno_temporal: str = "blancas"

        # Reproducir todos los movimientos para reconstruir el estado del tablero
        for indice, movimiento in enumerate(movimientos):
            coords: tuple[tuple[int, int], tuple[int, int]] | None = (
                f_parsear_movimiento(movimiento)
            )

            if coords is None:
                return ResultadoCarga(exito=False, razon_fallo="invalido")

            origen: tuple[int, int]
            destino: tuple[int, int]
            origen, destino = coords

            motivo: str = tablero_temporal.f_validar_movimiento(
                origen, destino, turno_temporal
            )
            if motivo != "":
                return ResultadoCarga(exito=False, razon_fallo="invalido")

            tablero_temporal.f_mover_pieza(origen, destino)

            color_rival: str = "negras" if turno_temporal == "blancas" else "blancas"
            rival_tiene_movs: bool = tablero_temporal.f_tiene_movimientos_validos(
                color_rival
            )

            if not rival_tiene_movs:
                # La partida terminó: solo es válido si era el último movimiento guardado
                if indice != len(movimientos) - 1:
                    return ResultadoCarga(exito=False, razon_fallo="invalido")
                return ResultadoCarga(exito=False, razon_fallo="terminada")

            turno_temporal = color_rival

        # Carga correcta: actualizar el estado interno con la partida restaurada
        self._tablero = tablero_temporal
        self._historial = list(movimientos)
        self._turno = turno_temporal
        return ResultadoCarga(exito=True)
