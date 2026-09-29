
#Constantes del tablero
TAMANO_TABLERO: int = 8
LETRAS_VALIDAS: str = "abcdefgh"
NUMEROS_VALIDOS: str = "12345678"
estado: str = "turno_blancas"

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

#Imprimir tablero
# for fila in tablero_simbolos:
#     print(fila)

    # Impresión del tablero con coordenadas usando bucles anidados
# print("  a b c d e f g h")
# for i in range(8):
#     numero_fila: int = 8 - i
#     print(f"{numero_fila}", end=" ")
#     for j in range(8):
#         print(f"{tablero_simbolos[i][j]}", end=" ")
#     print()  # Salto de línea al terminar cada fila

# print()  # Línea en blanco de separación

#imprimir tablero según profe
encabezado:str = " "
for indice_columna in range(TAMANO_TABLERO):
    letra_columna: str = LETRAS_VALIDAS[indice_columna]
    encabezado: str = encabezado + " " + letra_columna + " "
print(encabezado)

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
 # Línea en blanco de separación

tablero_nombres: list[list[str]] = [
    ["Torre negra", "Caballo negra", "Alfil negro", "Dama negra", "Rey negro", "Alfil negro", "Caballo negro", "Torre negra"],
    ["Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro", "Peón negro"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco", "Peón blanco"],
    ["Torre blanca", "Caballo blanca", "Alfil blanco", "Dama blanca", "Rey blanco", "Alfil blanco", "Caballo blanco", "Torre blanca"]
]

while estado != "salir":
    if estado == "turno_blancas":
        print("Turno de las blancas")
        casilla: str = input("Ingrese la casilla a consultar (o salir para terminar): ")
        if casilla == "salir":
            estado = "salir"
        elif len(casilla) == 2 and casilla[0] in LETRAS_VALIDAS and casilla[1] in NUMEROS_VALIDOS:
            # Buscar en que puesto de la matriz está para ver que ficha hay
            columna: int = LETRAS_VALIDAS.index(casilla[0])
            fila: int = 8 - int(casilla[1])
            
            contenido: str = tablero_nombres[fila][columna]
            
            if contenido != "":
                print(f"Hay un/a {contenido} en {casilla}.")
            else:
                print(f"La casilla {casilla} está vacía.")
           # print(f"La casilla {casilla} contiene {tablero_nombres[0][0]}")
            estado = "turno_negras"
        else:
            print("Casilla inválida")
    else:
        print("Turno de las negras")
        casilla: str = input("Ingrese la casilla a consultar (o salir para terminar): ")
        if casilla == "salir":
            estado = "salir"
        elif len(casilla) == 2 and casilla[0] in LETRAS_VALIDAS and casilla[1] in NUMEROS_VALIDOS:
            # Buscar en que puesto de la matriz está para ver que ficha hay
            columna: int = LETRAS_VALIDAS.index(casilla[0])
            fila: int = 8 - int(casilla[1])
            
            contenido: str = tablero_nombres[fila][columna]
            
            if contenido != "":
                print(f"Hay un/a {contenido} en {casilla}.")
            else:
                print(f"La casilla {casilla} está vacía.")
           # print(f"La casilla {casilla} contiene {tablero_nombres[0][0]}")
            estado = "turno_blancas"
        else:
            print("Casilla inválida")