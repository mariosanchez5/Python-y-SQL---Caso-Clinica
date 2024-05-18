from src.paciente import Paciente
from src.habitacion import Habitacion
from src.examen import Examen
from src.medico import Medico
from src.diagnostico import Diagnostico
from src.cama import Cama

habitaciones = []
pacientes = []
examenes = []
medicos = []
cama = []
diagnosticos = []

# Pacientes

def agregar_paciente(paciente):
    pacientes.append(paciente)


def quitar_paciente(paciente):
    # Desasignar paciente de cama
    for habitacion in habitaciones:
        if paciente.cama in habitacion.camas:
            habitacion.camas.remove(paciente.cama)
    # Desasignar paciente de médico
    if paciente.medico_tratante:
        for medico in medicos:
            if medico == paciente.medico_tratante:
                medico.quitar_paciente(paciente)
    pacientes.remove(paciente)


def obtener_paciente_por_rut(rut):
    for paciente in pacientes:
        if paciente.rut == rut:
            return paciente
    return None


def obtener_pacientes():
    return pacientes



# Médicos
def agregar_medico(medico):
    medicos.append(medico)


def quitar_medico(medico):
    medicos.remove(medico)


def obtener_medico_por_rut(rut):
    for medico in medicos:
        if medico.rut == rut:
            return medico
    return None


def obtener_medicos():
    return medicos



# Habitaciones
def agregar_habitacion(habitacion):
    habitaciones.append(habitacion)


def obtener_habitacion_por_id(id):
    for habitacion in habitaciones:
        if habitacion.id == id:
            return habitacion
    return None


def obtener_habitaciones():
    return habitaciones 


# Camas
def agregar_cama(cama, id_habitacion):
    habitacion = obtener_habitacion_por_id(id_habitacion)
    habitacion.agregar_cama(cama)


def obtener_cama_por_id(id):
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            if cama.id == id:
                return cama
    return None


def obtener_camas():
    camas = []
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            camas.append(cama)
    return camas


def obtener_camas_disponibles():
    camas = []
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            if cama.disponible:
                camas.append(cama)
    return camas


def obtener_una_cama_disponible():
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            if cama.disponible:
                return cama
    return None


# Exámenes
def agregar_examen(examen):
    examenes.append(examen)


def obtener_examen_por_id(id):
    for examen in examenes:
        if examen.id == id:
            return examen
    return None


def obtener_examenes_por_paciente(paciente):
    examenes_paciente = []
    for examen in examenes:
        if examen.paciente == paciente:
            examenes_paciente.append(examen)
    return examenes_paciente

def obtener_examenes():
    return examenes