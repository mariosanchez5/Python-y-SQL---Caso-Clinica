from funciones import *
from src.auxiliares import mostrar_menu, limpiar_pantalla

def main():
    opciones_validas = [ "Ver pacientes de la clínica",
                         "Mostrar paciente por RUT",
                         "Cambiar a paciente de cama",
                         "Cambiar a paciente de médico",
                         "Crear camas y habitaciones",
                         "Salir"]
    
    titulo = "Gestión hospitalaria"
    
    
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
            read = input("Presione enter para continuar")
        else:
            print("Hasta luego")
            break
        limpiar_pantalla()

if __name__ == "__main__":
    main()