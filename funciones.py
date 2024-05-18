from src.dummy_repositorio_clinica import *
from src.inicializacion import *

inicializar_datos()

def mostrar_pacientes():
    pacientes = obtener_pacientes()
    for paciente in pacientes:
        print(paciente.to_dict())


def mostrar_paciente_por_rut():
    rut = input("Ingrese el RUT del paciente sin puntos con guión: ")
    paciente = obtener_paciente_por_rut(rut)
    if paciente:
        print(paciente.to_dict())
    else:
        print("Paciente no encontrado")

def cambiar_paciente_cama():
    rut = input("Ingrese el RUT del paciente sin puntos con guión: ")
    paciente = obtener_paciente_por_rut(rut)
    # Caso 1: Paciente no existe
    if not paciente:
        print("Paciente no encontrado")
        return
    # Caso 2: Paciente existe y no tiene cama
    if not paciente.cama:        
        print("Paciente no tiene cama asignada.")
        id_cama = int(input("Ingrese el ID de la cama: "))
        paciente.cama = id_cama
    # Caso 3: Paciente existe y tiene cama
    else:
        id_cama = int(input("Ingrese el nuevo ID de la nueva cama: "))
        # Desasignar cama
        
    else:
        print("Paciente no encontrado")


def CambiarCama():
    #Por ahora lo dejaremos simple
    id_paciente = int(input('Ingresa el id del paciente a cambiar de cama: '))
    id_cama = int(input('Ingresa el id de la nueva cama: '))
    CambiarPacienteCama(id_cama, id_paciente)

def CambiarMedico():
    #Por ahora lo dejaremos simple
    id_paciente = int(input('Ingresa el id del paciente a cambiar de medico: '))
    id_medico = int(input('Ingresa el id del medico: '))
    CambiarPacienteCama(id_paciente, id_medico)

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
    
def validar_rut(rut):
    rut = rut.replace(".", "")
    rut = rut.replace("-", "")
    if len(rut) < 8:
        return False
    try:
        int(rut[:-1])
    except:
        return False
    return True