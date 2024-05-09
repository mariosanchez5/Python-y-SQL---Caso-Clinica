from funciones import *

def Main():
    while True:
        opcion = int(input('Ingresa 1 para ver los pacientes de la clinica\nIngresa 2 para mostrar el detalle de un paciente\nIngresa 3 para cambiar a un paciente de cama\nIngresa 4 para cambiar a un paciente de medico\nIngresa 5 para crear camas y habitaciones\nIngresa 6 para salir: \n'))

        if opcion == 1:
            MostrarTodos()
        elif opcion == 2:
            MostrasUnPaciente()
        elif opcion == 3:
            CambiarCama()
        elif opcion == 4:
            CambiarMedico()
        elif opcion == 5:
            CrearCamaYHabitacion()
        elif opcion == 6:
            break
        else:
            print('Opción Incorrecta')

Main()