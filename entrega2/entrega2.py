
#************************
# Constantes del tablero:
#************************

# Para el tamaño del tablero se usa la constante TAMANO_TABLERO = 8 para más adelante crear el tablero (8x8)
TAMANO_TABLERO: int = 8
# Para hacer luego la validación de si la casilla ingresada es válida, se crean estas constantes y luego preguntamos si la letra y el número de la casilla ingresada están en estas.
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"
# Definimos el estado inicial en turno_blancas para que siempre empiecen estas.
estado: str = "turno_blancas"

# *********************************************************************
# Crear las matrices  de nombres y símbolos que representan el tablero.
# *********************************************************************

# Crear el tablero con los símbolos de las piezas
tablero_simbolos: list[list[str]] = [
   ["\u265C", "\u265E", "\u265D", "\u265B", "\u265A", "\u265D", "\u265E", "\u265C"], # fila 8 (piezas negras)
   ["\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F", "\u265F"],  # fila 7 (peones negros)
   ["", "", "", "", "", "", "", ""],  # fila 6 (vacía)
   ["", "", "", "", "", "", "", ""],  # fila 5 (vacía)
   ["", "", "", "", "", "", "", ""],  # fila 4 (vacía)
   ["", "", "", "", "", "", "", ""],  # fila 3 (vacía)
   ["\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659", "\u2659"],  # fila 2 (peones blancos)
   ["\u2656", "\u2658", "\u2657", "\u2655", "\u2654", "\u2657", "\u2658", "\u2656"],  # fila 1 (piezas blancas)
]

# Crear el tablero con los nombres de las piezas
# Para luego consultar a este que pieza se encuentra en cada casilla.
tablero_nombres: list[list[str]] = [
    ["Torre negra", "Caballo negro", "Alfil negro", "Dama negra", "Rey negro", "Alfil negro", "Caballo negro", "Torre negra"],
    ["Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco"],
    ["Torre blanca", "Caballo blanco", "Alfil blanco", "Dama blanca", "Rey blanco", "Alfil blanco", "Caballo blanco", "Torre blanca"]
]

# **********
# Funciones
# **********

def f_validacion_casilla(casilla: str) -> bool:
    return len(casilla) == 2 and casilla[0] in LETRAS_VALIDAS and casilla[1] in NUMEROS_VALIDOS

def f_conversion_coordenadas(casilla: str) -> tuple[int, int]:
    # Busca en que puesto de la matriz está la casilla ingresada para ver que ficha hay
                # Coge el primer caracter de la casilla ingresada y busca en que posición de LETRAS_VALIDAS está para saber en que columna de la matriz está 
                columna: int = LETRAS_VALIDAS.index(casilla[0])
                # Coge el segundo caracter de la casilla ingresada y lo combierte en entero. Luego le resta 8 para saber en que fila de la matriz está.
                fila: int = 8 - int(casilla[1])
    
                # Busca en la matriz tablero_nombres en la fila y columna que se ha calculado para ver que ficha hay en esa casilla y lo guarda en una variable.
                return fila, columna


def f_consulta_pieza(fila:int, columna:int) -> str:
    return tablero_nombres[fila][columna]

def f_imprimir_tablero(tablero: list[list[str]]) -> None:
    encabezado:str = " "
for indice_columna in range(TAMANO_TABLERO):
    letra_columna: str = LETRAS_VALIDAS[indice_columna]
    encabezado: str = encabezado + " " + letra_columna + " "
print(encabezado)

# Recorre cada fila imprimiendo el número de la fila y los símbolos correspondientes a las fichas de cada casilla o un punto si no hay ninguna ficha.
for indice_fila in range(TAMANO_TABLERO):
    numero_fila: int = TAMANO_TABLERO - indice_fila
    linea: str = str(numero_fila)
    for indice_columna in range(TAMANO_TABLERO):
        simbolo: str = tablero_simbolos[indice_fila][indice_columna]
        if simbolo == "":
            celda: str = " . "
        else:
            celda: str = " " + simbolo + " "
        linea: str = linea + celda
    print(linea)



# *******************
# Imprimir el tablero
# *******************

f_imprimir_tablero(tablero_simbolos)


# ****************************
# Hacer la dinámica del juego:
# ****************************

# Empiezan las blancas porque al declarar la variable estado he puesto que contiene turno_blancas
# Muestra de quien es el turno y pide que ingreses una casilla.
# Si escriben salir, cambia el estado a "salir" y acabe el juego ya que en el while pone que se repita hasta que el estado sea igual a salir.
# Si insertan una casilla que no sea válida, muestra un mensaje de "Casilla inválida", sigue en el turno de quien le tocaba y vuelve a pedirte una casilla.
# Si insertan una casilla válida, muestra que pieza está en esa casilla y cambia el estado al turno del otro jugador.

while estado != "salir":
    if estado == "turno_blancas":
        print("Turno de las blancas")
        casilla: str = input("Ingrese la casilla a consultar (o salir para terminar): ")
        if casilla == "salir":
            estado = "salir"

        # Si la el texto ingresado tiene dos caracteres y el primero es una letra guardada en la constante LETRAS_VALIDAS y el segundo es un número guardado en la constante NUMEROS_VALIDOS te dice que pieza hay en la casilla y cambia el turno, sinó te da el mensaje de cailla inválida y vuelve a pedir la casilla.
        elif f_validacion_casilla(casilla):
            # Busca en que puesto de la matriz está la casilla ingresada para ver que ficha hay
            fila, columna = f_conversion_coordenadas(casilla)
            # Busca en la matriz tablero_nombres en la fila y columna que se ha calculado para ver que ficha hay en esa casilla y lo guarda en una variable.
            contenido: str = f_consulta_pieza(fila, columna)

            # Si la casilla no está vacía te dice que pieza hay, sinó te dice que la casilla está vacía y cambia el turno a el otro jugador.
            if contenido != "":
                print(f"Hay un/a {contenido} en {casilla}.")
            else:
                print(f"La casilla {casilla} está vacía.")
            estado = "turno_negras"
        else:
            print("Casilla inválida")

   #Cuando el estado cambia a turno_negras se hace lo mismo para el turno de las negras.
    else:
        print("Turno de las negras")
        casilla: str = input("Ingrese la casilla a consultar (o salir para terminar): ")
        if casilla == "salir":
            estado = "salir"
        elif f_validacion_casilla(casilla):
            fila, columna = f_conversion_coordenadas(casilla)
            contenido: str = f_consulta_pieza(fila, columna)

            if contenido != "":
                print(f"Hay un/a {contenido} en {casilla}.")
            else:
                print(f"La casilla {casilla} está vacía.")
            estado = "turno_blancas"
        else:
            print("Casilla inválida")