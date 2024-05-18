from src.paciente import Paciente
from src.habitacion import Habitacion
from src.examen import Examen
from src.medico import Medico
from src.diagnostico import Diagnostico
from src.cama import Cama
import psycopg2
import config

conexion = None

def ObtenerConexion():
    if conexion is None:
        conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    return conexion    

"""
habitaciones = []
pacientes = []
examenes = []
medicos = []
cama = []
diagnosticos = []
"""

# Pacientes
def guardar_paciente(paciente):
    conexion = ObtenerConexion()
    cursor = conexion.cursor()
    p = obtener_paciente_por_rut(paciente.rut)
    if p:
        cursor.execute("DELETE FROM pacientes WHERE rut = %s", (p,))
    cursor.execute("INSERT INTO pacientes (nombre, apellido, rut, medicos_id, camas_id) VALUES (%s, %s, %s, %s, %s)", (paciente.nombre, paciente.apellido, paciente.rut, paciente.medicos_id, paciente.camas_id))
    conexion.commit()
    conexion.close()


def quitar_paciente(paciente):
    habitaciones = []
    pacientes = []
    medicos = []
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
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    select_filter_paciente = cursor.execute("SELECT * FROM pacientes WHERE rut = %s",(rut,))
    if select_filter_paciente.rowcount > 0:
        row = select_filter_paciente.fetchone()
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-Edad:',str(row[4]),'-Genero:',str(row[5]))
            row = select_filter_paciente.fetchone()
    else:
        print('No existen registros en la base de datos')

    conexion.close()


def obtener_pacientes():
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    all_pacientes = cursor.execute("SELECT * FROM pacientes")
    if all_pacientes.rowcount > 0: 
        row = all_pacientes.fetchone() 
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-medicos_id:',str(row[4]),'-camas_id:',str(row[5]))
            row = all_pacientes.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()



# Médicos
def guardar_medico(medico):
    conexion = ObtenerConexion()
    cursor = conexion.cursor()
    m = obtener_medico_por_rut(medico.rut)
    if m:
        cursor.execute("DELETE FROM medicos WHERE rut = %s", (m,))
    cursor.execute("INSERT INTO medicos (nombre, apellido, rut) VALUES (%s, %s, %s)", (medico.nombre, medico.apellido, medico.rut))
    conexion.commit()
    conexion.close()


def quitar_medico(medico):
    medicos = []
    medicos.remove(medico)


def obtener_medico_por_rut(rut):
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    select_filter_medico = cursor.execute("SELECT * FROM medicos WHERE rut = %s",(rut,))
    if select_filter_medico.rowcount > 0:
        row = select_filter_medico.fetchone()
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]))
            row = select_filter_medico.fetchone()
    else:
        print('No existen registros en la base de datos')

    conexion.close()


def obtener_medicos():
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    all = cursor.execute("SELECT * FROM medicos")
    if all.rowcount > 0: 
        row = all.fetchone() 
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]))
            row = all.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()



# Habitaciones
def guardar_habitacion(habitacion):
    conexion = ObtenerConexion()
    cursor = conexion.cursor()
    h = obtener_habitacion_por_id(habitacion.id)
    if h:
        cursor.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (h,))
    cursor.execute("INSERT INTO habitaciones (id_habitacion) VALUES (%s)", (habitacion.id))
    conexion.commit()
    conexion.close()


def obtener_habitacion_por_id(id):
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    select_filter_habitacion = cursor.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s",(id,))
    if select_filter_habitacion.rowcount > 0:
        row = select_filter_habitacion.fetchone()
        while row is not None:
            print('Habitacion :',str(row[0]))
            row = select_filter_habitacion.fetchone()
    else:
        print('No existen registros en la base de datos')

    conexion.close()


def obtener_habitaciones():
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    all = cursor.execute("SELECT * FROM habitaciones")
    if all.rowcount > 0: 
        row = all.fetchone() 
        while row is not None:
            print('Habitacion :',str(row[0]))
            row = all.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()


# Camas
def guardar_cama(cama):
    c = obtener_cama_por_id(cama.id)
    if c:
        habitacion = obtener_habitacion_por_id(cama.habitacion.id)
        habitacion.camas.remove(c)
    habitacion = obtener_habitacion_por_id(cama.habitacion.id)
    habitacion.agregar_cama(cama)


def obtener_cama_por_id(id):
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    select_filter_cama = cursor.execute("SELECT * FROM camas WHERE id_cama = %s",(id,))
    if select_filter_cama.rowcount > 0:
        row = select_filter_cama.fetchone()
        while row is not None:
            print('Cama :',str(row[0]),'disponible :',str(row[1]),'habitaciones_id :',str(row[2]))
            row = select_filter_cama.fetchone()
    else:
        print('No existen registros en la base de datos')

    conexion.close()


def obtener_camas():
    habitaciones = []
    camas = []
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            camas.append(cama)
    return camas


def obtener_camas_disponibles():
    habitaciones = []
    camas = []
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            if cama.disponible:
                camas.append(cama)
    return camas


def obtener_una_cama_disponible():
    habitaciones = []
    for habitacion in habitaciones:
        for cama in habitacion.camas:
            if cama.disponible:
                return cama
    return None


# Exámenes
def guardar_examen(examen):
    examenes = []
    e = obtener_examen_por_id(examen.id)
    if e:
        examenes.remove(e)
    examenes.append(examen)


def obtener_examen_por_id(id):
    examenes = []
    for examen in examenes:
        if examen.id == id:
            return examen
    return None


def obtener_examenes_por_paciente(paciente):
    examenes = []
    examenes_paciente = []
    for examen in examenes:
        if examen.paciente == paciente:
            examenes_paciente.append(examen)
    return examenes_paciente

def obtener_examenes():
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    all = cursor.execute("SELECT * FROM medicos")
    if all.rowcount > 0: 
        row = all.fetchone() 
        while row is not None:
            print('Nombre :',str(row[1]), '-Resultado :', str(row[2]), '-medicos_id; ',str(row[3]),'-pacientes_id; ',str(row[4],'-fecha; ',str(row[5])))
            row = all.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()
    

# Diagnósticos
def guardar_diagnostico(diagnostico):
    diagnosticos = []
    d = obtener_diagnostico_por_paciente(diagnostico.paciente)
    if d:
        diagnosticos.remove(d)
    diagnosticos.append(diagnostico)


def obtener_diagnostico_por_paciente(paciente):
    diagnosticos = []
    for diagnostico in diagnosticos:
        if diagnostico.paciente == paciente:
            return diagnostico
    return None


def obtener_diagnosticos():
    conexion = ObtenerConexion()
    cursor = conexion.cursor()

    all = cursor.execute("SELECT * FROM medicos")
    if all.rowcount > 0: 
        row = all.fetchone() 
        while row is not None:
            print('medicos_id :',str(row[1]), '-pacientes_id :', str(row[2]), '-enfermedad; ',str(row[3]))
            row = all.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()