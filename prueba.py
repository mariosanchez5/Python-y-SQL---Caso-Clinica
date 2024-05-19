rut = "19.091.111-5"

# def rut_a_int(rut):
#     if rut is None: return None
#     rut_sin_dv = rut[:-2]
#     sin_puntos = rut_sin_dv.replace(".", "")
#     return int(sin_puntos)

# print(rut_a_int(rut))

def eliminar_puntos_guiones_a_entero(rut):
    numero_sin_formato = rut.replace(".", "").replace("-", "")
    # Convertir la cadena a entero
    numero_entero = int(numero_sin_formato)
    
    return numero_entero

print(eliminar_puntos_guiones_a_entero(rut))
