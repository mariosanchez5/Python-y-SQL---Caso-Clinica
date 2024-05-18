from src.repositorio_clinica import *
from src.inicializacion import *

inicializar_datos()

###### AUXILIARES ######
def solicitar_cama_por_id():
    id_cama = int(input("Ingrese el ID de la cama: "))
    cama = obtener_cama_por_id(id_cama)
    if cama:
        if cama.disponible:
            return cama
    print("Cama no encontrada o no disponible") 
    return None


def solicitar_paciente():
    rut = input("Ingrese el RUT del paciente sin puntos con guión: ")
    paciente = obtener_paciente_por_rut(rut)
    if not paciente:
        print("Paciente no registrado")
        return None
    return paciente


def solicitar_medico():
    rut = input("Ingrese el RUT del médico sin puntos con guión: ")
    medico = obtener_medico_por_rut(rut)
    if not medico:
        print("Médico no registrado")
        return None
    return medico

#########################


def mostrar_pacientes():
    pacientes = obtener_pacientes()
    for paciente in pacientes:
        print(paciente.to_dict())


def mostrar_paciente_por_rut():
    paciente = solicitar_paciente() 
    if paciente:
        print(paciente.to_dict())
    else:
        print("Paciente no encontrado")


def cambiar_paciente_cama():
    paciente = solicitar_paciente()
    if not paciente: return
    # Hasta acá se ha validado que el paciente existe
    cama_asignada = solicitar_cama_por_id()
    if not cama_asignada: return
    # Hasta acá se ha validado que el paciente existe y la cama está disponible
    if paciente.cama:
        cama_actual = obtener_cama_por_id(paciente.cama)
        cama_actual.desocupar()
        guardar_cama(cama_actual)
    paciente.asignar_cama(cama_asignada)
    cama_asignada.ocupar()
    guardar_paciente(paciente)
    guardar_cama(cama_asignada)
    print("Cama asignada correctamente")
    return


def cambiar_paciente_medico():
    paciente = solicitar_paciente()
    if not paciente: return
    medico = solicitar_medico()
    if not medico: return
    # Hasta acá se ha validado que el paciente y el médico existen
    if paciente.medico_tratante:
        medico_actual = obtener_medico_por_rut(paciente.medico_tratante.rut)
        medico_actual.quitar_paciente(paciente)
        guardar_medico(medico_actual)
    paciente.asignar_medico(medico)
    medico.agregar_paciente(paciente)
    guardar_paciente(paciente)
    guardar_medico(medico)
    print("Médico asignado correctamente")
    return



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