"""Prueba rápida de arranque: comprueba que todas las clases y métodos se ejecutan sin excepciones."""

from modelo.Pieza import Pieza
from modelo.Torre import Torre
from modelo.Caballo import Caballo
from modelo.Alfil import Alfil
from modelo.Reina import Reina
from modelo.Rey import Rey
from modelo.Peon import Peon
from modelo.Tablero import Tablero


def probar_sin_errores() -> None:
    """Instancia todas las clases y llama a sus métodos sin comprobar la lógica."""
    tablero: Tablero = Tablero()
    tablero.imprimir_tablero()
    _ = tablero.obtener_pieza((6, 4))
    _ = tablero.camino_libre((7, 0), (5, 0))
    tablero.mover_pieza((6, 4), (4, 4))
    _ = tablero.buscar_rey("blancas")
    _ = tablero.casilla_atacada((0, 0), "blancas")
    _ = tablero.esta_en_jaque("blancas")
    _ = tablero.deja_rey_en_jaque((7, 4), (6, 4), "blancas")
    _ = tablero.validar_movimiento((4, 4), (3, 4), "blancas")
    _ = tablero.tiene_movimientos_validos("blancas")

    piezas: list[Pieza] = [
        Pieza("blancas", "?", "generica"),
        Torre("blancas"),
        Caballo("blancas"),
        Alfil("blancas"),
        Reina("blancas"),
        Rey("blancas"),
        Peon("blancas"),
        Torre("negras"),
        Caballo("negras"),
        Alfil("negras"),
        Reina("negras"),
        Rey("negras"),
        Peon("negras"),
    ]

    for pieza in piezas:
        _ = pieza.es_movimiento_valido(tablero, (6, 0), (5, 0))

    print("Todo se ha ejecutado sin errores.")


if __name__ == "__main__":
    probar_sin_errores()