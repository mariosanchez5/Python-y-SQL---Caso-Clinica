from src.funciones import *
from src.auxiliares import mostrar_menu, limpiar_pantalla
from src.repositorio_clinica import conexion, obtener_pacientes,\
    obtener_camas, obtener_medicos, obtener_habitaciones,\
    obtener_examenes, obtener_diagnosticos

def main():
    opciones_validas = [ "Ver pacientes de la clínica",
                         "Mostrar paciente por RUT",
                         "Cambiar a paciente de cama",
                         "Cambiar a paciente de médico",
                         "Crear camas y habitaciones",
                         "Otras acciones",
                         "Salir"]
    
    titulo = "Sistema de gestión hospitalaria"
    
    while True: 
        opcion = mostrar_menu(titulo, opciones_validas, "Ingrese el número de la opción deseada: ")
        
        if opcion == "1":
            mostrar_pacientes()
            read = input("Presione enter para continuar")
        elif opcion == "2":
            mostrar_paciente_por_rut()
            read = input("Presione enter para continuar")
        elif opcion == "3":
            cambiar_paciente_cama()
            read = input("Presione enter para continuar")
        elif opcion == "4":
            cambiar_paciente_medico()
            read = input("Presione enter para continuar")
        elif opcion == "5":
            crear_camas_y_habitaciones()
        elif opcion == "6":
            acciones_adicionales(mostrar_menu("Otras opciones", ["Ver médicos", "Ver camas", "Ver habitaciones", "Ver exámenes", "Ver diagnósticos", "Volver atrás"], "Ingresa la opción deseada: "))
        else:
            print("Hasta luego")
            break
        limpiar_pantalla()


def acciones_adicionales(opcion):
    if opcion == "1":
        resultado = mostrar_medicos()
    elif opcion == "2":
        resultado = mostrar_camas()
    elif opcion == "3":
        resultado = mostrar_habitaciones()
    elif opcion == "4":
        resultado = mostrar_examenes()
    elif opcion == "5":
        resultado = mostrar_diagnosticos()
    elif opcion == "6":
        return
    else:
        print("Opción no válida")
    #for r in resultado: print(r.to_dict())
    input("Presione enter para continuar")
    limpiar_pantalla()


if __name__ == "__main__":
    main()