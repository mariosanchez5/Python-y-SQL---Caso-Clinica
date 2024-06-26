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
camas = []
diagnosticos = []

conexion = None

# Pacientes
def guardar_paciente(paciente):
    p = obtener_paciente_por_rut(paciente.rut)
    if p:
        pacientes.remove(p)
    pacientes.append(paciente)


def quitar_paciente(paciente):
    for p in pacientes:
        if p == paciente:
            pacientes.remove(paciente)


def obtener_paciente_por_rut(rut):
    for paciente in pacientes:
        if paciente.rut == rut:
            return paciente
    return None


def obtener_pacientes():
    return pacientes



# Médicos
def guardar_medico(medico):
    m = obtener_medico_por_rut(medico.rut)
    if m:
        medicos.remove(m)
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
def guardar_habitacion(habitacion):
    h = obtener_habitacion_por_id(habitacion.id)
    if h:
        habitaciones.remove(h)
    habitaciones.append(habitacion)


def obtener_habitacion_por_id(id):
    for habitacion in habitaciones:
        if habitacion.id == id:
            return habitacion
    return None


def obtener_habitaciones():
    return habitaciones 


# Camas
def guardar_cama(cama):
    c = obtener_cama_por_id(cama.id)
    if c:
        camas.remove(c)
    camas.append(cama)


def obtener_cama_por_id(id):
    for cama in camas:
        if cama.id == id:
            return cama
    return None


def obtener_camas():
    return camas


def obtener_camas_disponibles():
    disponibles = []
    for cama in camas:
        if cama.disponible:
            disponibles.append(cama)
    return disponibles


def obtener_una_cama_disponible():
    for cama in camas:
        if cama.disponible:
            return cama
    return None


def obtener_paciente_por_cama(cama):
    for paciente in pacientes:
        if paciente.id_cama == cama.id:
            return paciente
    return None 


# Exámenes
def guardar_examen(examen):
    e = obtener_examen_por_id(examen.id)
    if e:
        examenes.remove(e)
    examenes.append(examen)


def obtener_examen_por_id(id):
    for examen in examenes:
        if examen.id == id:
            return examen
    return None


def obtener_examenes_por_paciente(paciente):
    examenes_paciente = []
    for examen in examenes:
        if examen.rut_paciente == paciente.rut:
            examenes_paciente.append(examen)
    return examenes_paciente

def obtener_examenes():
    return examenes
    

# Diagnósticos
def guardar_diagnostico(diagnostico):
    d = obtener_diagnostico_por_id(diagnostico.id)
    if d:
        diagnosticos.remove(d)
    diagnosticos.append(diagnostico)


def obtener_diagnostico_por_id(id):
    for diagnostico in diagnosticos:
        if diagnostico.id == id:
            return diagnostico
    return None


def obtener_diagnosticos_por_paciente(paciente):
    for diagnostico in diagnosticos:
        if diagnostico.rut_paciente == paciente.rut:
            yield diagnostico
    return None


def obtener_diagnosticos():
    return diagnosticos