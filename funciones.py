from clases import *
from models import *

def MostrarTodos():
    VerTodosPacientes()

def MostrasUnPaciente():
    rut = input("Ingrese el Rut del paciente sin puntos ni guion: ")
    FiltrarPacientes(rut)

def CambiarCama():
    pass

def CambiarMedico():
    pass

def CrearCamaYHabitacion():
    opcion = int(input('Ingresa 1 si deseas crear una cama, Ingresa 2 si deseas crear una habitación'))
    if opcion == 1:
        ncamas = int(input('Cuantas camas deseas crear: '))
        CrearCamas(ncamas)
    elif opcion == 2:
        zona = input('Ingresa la zona donde deseas crear la habitacion: ')
        ncamas2 = int(input('Ingresa el número de camas de la nueva habitación: '))
        CrearHabitaciones(ncamas2,zona)
    else:
        print('Opción incorrecta')