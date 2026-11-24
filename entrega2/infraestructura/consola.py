"""
Capa de infraestructura: interacción con el usuario a través de la consola.
Gestiona la visualización del tablero, la lectura de comandos y la presentación
de resultados. No contiene ninguna lógica de negocio ni acceso directo a archivos.
"""

from pathlib import Path

from dominio.Pieza import Pieza
from dominio.Tablero import Tablero
from aplicacion.partida_service import (
    PartidaService,
    ResultadoMovimiento,
    ResultadoCarga,
    f_parsear_movimiento,
)
from infraestructura.persistencia_ficheros import (
    f_guardar_historial,
    f_cargar_historial,
    f_exportar_historial_csv,
)

# Rutas de los archivos de persistencia
RUTA_PARTIDA: Path = Path("partida.txt")
RUTA_CSV: Path = Path("partida.csv")

# Constantes de visualización del tablero
LETRAS_COLUMNAS: str = "abcdefgh"
TAMANO_TABLERO: int = 8


def f_imprimir_tablero(tablero: Tablero) -> None:
    """
    Imprime el tablero por consola con coordenadas a-h y 1-8 (fila 8 arriba).

    Parámetros:
        tablero: tablero cuyo estado se quiere mostrar por pantalla.
    """
    # Construir la cabecera con las letras de columna
    encabezado: str = " "
    for indice_columna in range(TAMANO_TABLERO):
        letra_columna: str = LETRAS_COLUMNAS[indice_columna]
        encabezado = encabezado + " " + letra_columna + " "
    print(encabezado)

    # Imprimir cada fila con su número a la izquierda
    for indice_fila in range(TAMANO_TABLERO):
        numero_fila: int = TAMANO_TABLERO - indice_fila
        linea: str = str(numero_fila)
        for indice_columna in range(TAMANO_TABLERO):
            pieza: Pieza | None = tablero.casillas[indice_fila][indice_columna]
            if pieza is None:
                celda: str = " . "
            else:
                celda = " " + pieza.simbolo + " "
            linea = linea + celda
        print(linea)


def f_gestionar_carga_partida(servicio: PartidaService) -> None:
    """
    Pregunta al usuario si desea cargar la partida guardada y aplica la carga si procede.

    Parámetros:
        servicio: instancia del servicio de partida que gestionará el estado cargado.
    """
    respuesta: str = input(
        "Existe una partida guardada. ¿Quieres continuarla? (s/n): "
    ).strip().lower()

    if respuesta == "s":
        movimientos_guardados: list[str] = f_cargar_historial(RUTA_PARTIDA)
        resultado_carga: ResultadoCarga = servicio.f_cargar_desde_movimientos(
            movimientos_guardados
        )

        if not resultado_carga.exito:
            if resultado_carga.razon_fallo == "terminada":
                print("La partida guardada ya había terminado. Se empieza una nueva.")
            else:
                print("El archivo guardado no es válido. Se empieza una partida nueva.")
        else:
            print("Partida cargada correctamente.")


def f_procesar_movimiento(servicio: PartidaService, entrada: str) -> bool:
    """
    Parsea, valida y ejecuta el movimiento introducido por el usuario.
    Guarda el historial y muestra el resultado por pantalla.

    Parámetros:
        servicio: instancia del servicio de partida.
        entrada: cadena introducida por el usuario (ej. 'e2 e4').
    Devuelve:
        True si la partida ha terminado tras el movimiento, False en caso contrario.
    """
    coords: tuple[tuple[int, int], tuple[int, int]] | None = (
        f_parsear_movimiento(entrada)
    )

    if coords is None:
        print("Formato no válido. Escribe origen y destino, por ejemplo: e2 e4")
        return False

    origen: tuple[int, int]
    destino: tuple[int, int]
    origen, destino = coords

    # Normalizar la notación antes de pasarla al servicio
    notacion: str = " ".join(entrada.split())
    partes: list[str] = notacion.split()

    resultado: ResultadoMovimiento = servicio.f_realizar_movimiento(
        origen, destino, notacion
    )

    if not resultado.exito:
        print(f"Movimiento rechazado: {resultado.motivo}")
        return False

    print(f"Movimiento realizado: {partes[0]} -> {partes[1]}")

    # Persistir el estado actualizado de la partida
    f_guardar_historial(servicio.f_obtener_historial(), RUTA_PARTIDA)

    f_imprimir_tablero(servicio.f_obtener_tablero())

    # Mostrar el resultado: jaque mate, tablas o jaque simple
    if resultado.jaque_mate:
        print(f"Jaque mate. Ganan las {resultado.ganador}.")
        return True

    if resultado.tablas:
        print("Tablas por rey ahogado.")
        return True

    # Tras un movimiento exitoso sin fin de partida, el turno ya cambió al rival;
    # si ese rival está en jaque, f_obtener_turno() devuelve su color directamente
    if resultado.jaque:
        print(f"Jaque a las {servicio.f_obtener_turno()}.")

    return False


def f_ejecutar_bucle_principal() -> None:
    """
    Bucle principal del juego: inicializa el servicio, gestiona la carga y ejecuta el juego.

    Coordina la interacción con el usuario delegando la lógica al servicio de partida
    y la persistencia al módulo correspondiente.
    """
    servicio: PartidaService = PartidaService()

    # Ofrecer cargar la partida guardada si existe un archivo previo
    if RUTA_PARTIDA.exists():
        f_gestionar_carga_partida(servicio)

    f_imprimir_tablero(servicio.f_obtener_tablero())

    partida_en_curso: bool = True

    while partida_en_curso:
        color_turno: str = servicio.f_obtener_turno()
        print(f"Turno de las {color_turno}")
        entrada: str = input(
            "Movimiento (ej. e2 e4), 'exportar' o 'salir': "
        ).strip().lower()

        if entrada == "salir":
            print("Fin de la partida.")
            partida_en_curso = False

        elif entrada == "exportar":
            f_exportar_historial_csv(servicio.f_obtener_historial(), RUTA_CSV)
            print("Historial exportado correctamente.")

        else:
            # Procesar el movimiento; si devuelve True, la partida ha terminado
            partida_terminada: bool = f_procesar_movimiento(servicio, entrada)
            if partida_terminada:
                partida_en_curso = False
