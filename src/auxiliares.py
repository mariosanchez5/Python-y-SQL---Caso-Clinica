# Reemplazo de input(), para permitir solo enteros
# positivos.
def ingresar_entero_positivo(mensaje):
    while True:
        numero = int(input(mensaje))
        if numero > 0 and numero == int(numero):
            return numero
        else:
            print("Debe ingresar un número entero positivo.")

# Reemplazo de input(), para permitir solo opciones
# válidas.
def ingresar_opcion_valida(mensaje, opciones):
    while True:
        opcion = input(mensaje)
        if opcion in opciones:
            return opcion
        else:
            print("Opción inválida. Intente nuevamente.\n")


# Imprime las opciones que recibe en una lista de strings
def mostrar_opciones(opciones):
    contador = 1
    for opcion in opciones:
        print(str(contador) + ". " + opcion)
        contador += 1
        
# Muestra un menú numérico, validando las opciones
# ingresadas.
def mostrar_menu(titulo, opciones, mensaje):
    print(titulo)
    print(len(titulo) * "-")
    mostrar_opciones(opciones)
    validas = []
    for i in range(len(opciones) + 1):
        validas.append(str(i))
    print()
    return ingresar_opcion_valida(mensaje, validas)

# Alinea un texto a la izquierda, derecha o centrado
def alinear_texto(texto, ancho, alineacion):
    if alineacion == "l":
        return texto.ljust(ancho)
    elif alineacion == "r":
        return texto.rjust(ancho)
    elif alineacion == "c":
        return texto.center(ancho)
    else:
        return texto


# Muestra una tabla
# columnas: lista de tuplas con el nombre de la columna, el ancho y la alineación
# filas: lista de tuplas con los valores de la fila
def mostrar_tabla(columnas, filas):
    # Cabecera
    cabecera = ""
    for columna in columnas:
        cabecera += alinear_texto(columna[0], columna[1], columna[2])
    print(cabecera)
    # Subrayado
    print(len(cabecera) * "-")
    # Filas
    for fila in filas:
        for i in range(len(fila)):
            print(alinear_texto(fila[i], columnas[i][1], columnas[i][2]), end="")
        print()
            
# Función para limpiar la pantalla. Simplemente imprime
# muchas líneas vacías.
def limpiar_pantalla():
    for i in range(100):
        print()


def int_a_rut(numero):
    if numero is None: return None
    rut = str(numero)
    # Calcula el dígito verificador
    # usando módulo 11
    suma = 0
    multiplicador = 2
    for i in range(1, len(rut) + 1):
        suma += int(rut[-i]) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    dv = 11 - (suma % 11)
    # Agregar puntos
    rut_con_puntos = ""
    for indice, digito in enumerate(rut[::-1]):
        if indice % 3 == 0 and indice > 0:
            rut_con_puntos += "."
        rut_con_puntos += digito
    return rut_con_puntos[::-1] + "-" + ("K" if dv == 10 else str(dv))


def rut_a_int(rut):
    if rut is None: return None
    rut_sin_dv = rut[:-2]
    sin_puntos = rut_sin_dv.replace(".", "")
    return int(sin_puntos)
