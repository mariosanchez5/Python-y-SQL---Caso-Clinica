from src.paciente import Paciente
from src.habitacion import Habitacion
from src.examen import Examen
from src.medico import Medico
from src.diagnostico import Diagnostico
from src.cama import Cama
import psycopg2
import config


########################
# Gestión de la conexión
conexion = None

def obtener_conexion():
    if conexion is None:
        conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    return conexion    

# Decorador para manejar la conexión segura
def conexion_segura(func):
    def wrapper(*args, **kwargs):
        # Se obtiene la conexión
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            return func(*args, **kwargs, cursor=cursor)
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.commit()
    return wrapper

########################################


# Pacientes
@conexion_segura
def guardar_paciente(paciente) -> None:
    cursor = kwargs['cursor']
    p = obtener_paciente_por_rut(paciente.rut)
    if p:
        cursor.execute("DELETE FROM pacientes WHERE rut = %s", (p,))
    cursor.execute("INSERT INTO pacientes (nombre, apellido, rut, medicos_id, camas_id) VALUES (%s, %s, %s, %s, %s)", (paciente.nombre, paciente.apellido, paciente.rut, paciente.medicos_id, paciente.camas_id))


@conexion_segura
def quitar_paciente(paciente) -> None:
    return None


@conexion_segura
def obtener_paciente_por_rut(rut) -> Paciente or None:
    #select_filter_paciente = cursor.execute("SELECT * FROM pacientes WHERE rut = %s",(rut,))
    return Paciente('dummy_nombre', 'dummy_apellido', '0000000-1', '1111111-2', '10000')


@conexion_segura
def obtener_pacientes() -> list[Paciente]:
    return []



# Médicos
@conexion_segura
def guardar_medico(medico) -> None:
    cursor = kwargs['cursor']
    # m = obtener_medico_por_rut(medico.rut)
    # if m:
    #     cursor.execute("DELETE FROM medicos WHERE rut = %s", (m,))
    # cursor.execute("INSERT INTO medicos (nombre, apellido, rut) VALUES (%s, %s, %s)", (medico.nombre, medico.apellido, medico.rut))
    return None
    

@conexion_segura
def quitar_medico(medico) -> None:
    cursor = kwargs['cursor']
    m = obtener_medico_por_rut(medico.rut)
    if m:
        cursor.execute("DELETE FROM medicos WHERE rut = %s", (m,))
    return None

@conexion_segura
def obtener_medico_por_rut(rut) -> Medico or None:
    cursor = kwargs['cursor'] 

    # select_filter_medico = cursor.execute("SELECT * FROM medicos WHERE rut = %s",(rut,))
    # if select_filter_medico.rowcount > 0:
    #     row = select_filter_medico.fetchone()
    #     while row is not None:
    #         print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]))
    #         row = select_filter_medico.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return None

@conexion_segura
def obtener_medicos() -> list[Medico]:
    cursor = kwargs['cursor']

    # all = cursor.execute("SELECT * FROM medicos")
    # if all.rowcount > 0: 
    #     row = all.fetchone() 
    #     while row is not None:
    #         print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]))
    #         row = all.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return []


# Habitaciones
@conexion_segura
def guardar_habitacion(habitacion) -> None:
    cursor = kwargs['cursor']
    
    # h = obtener_habitacion_por_id(habitacion.id)
    # if h:
    #     cursor.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (h,))
    # cursor.execute("INSERT INTO habitaciones (id_habitacion) VALUES (%s)", (habitacion.id))
    return None


@conexion_segura
def obtener_habitacion_por_id(id) -> Habitacion or None:
    cursor = kwargs['cursor']

    # select_filter_habitacion = cursor.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s",(id,))
    # if select_filter_habitacion.rowcount > 0:
    #     row = select_filter_habitacion.fetchone()
    #     while row is not None:
    #         print('Habitacion :',str(row[0]))
    #         row = select_filter_habitacion.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return None


@conexion_segura
def obtener_habitaciones():
    cursor = kwargs['cursor']

    all = cursor.execute("SELECT * FROM habitaciones")
    if all.rowcount > 0: 
        row = all.fetchone() 
        while row is not None:
            print('Habitacion :',str(row[0]))
            row = all.fetchone()
    else:
        print('No existen registros en la base de datos')


# Camas
def guardar_cama(cama):
    c = obtener_cama_por_id(cama.id)
    if c:
        habitacion = obtener_habitacion_por_id(cama.habitacion.id)
        habitacion.camas.remove(c)
    habitacion = obtener_habitacion_por_id(cama.habitacion.id)
    habitacion.agregar_cama(cama)

@conexion_segura
def obtener_cama_por_id(id) -> Cama or None:
    cursor = kwargs['cursor']

    # select_filter_cama = cursor.execute("SELECT * FROM camas WHERE id_cama = %s",(id,))
    # if select_filter_cama.rowcount > 0:
    #     row = select_filter_cama.fetchone()
    #     while row is not None:
    #         print('Cama :',str(row[0]),'disponible :',str(row[1]),'habitaciones_id :',str(row[2]))
    #         row = select_filter_cama.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return None


def obtener_camas() -> list[Cama]:
    return []


def obtener_camas_disponibles() -> list[Cama]:
    return []


def obtener_una_cama_disponible() -> Cama or None:
    return None


# Exámenes
def guardar_examen(examen) -> None:
    return None


def obtener_examen_por_id(id) -> Examen or None:
    return None


def obtener_examenes_por_paciente(paciente) -> list[Examen]:
    return []

@conexion_segura
def obtener_examenes() -> list[Examen]:
    cursor = kwargs['cursor']

    # all = cursor.execute("SELECT * FROM medicos")
    # if all.rowcount > 0: 
    #     row = all.fetchone() 
    #     while row is not None:
    #         print('Nombre :',str(row[1]), '-Resultado :', str(row[2]), '-medicos_id; ',str(row[3]),'-pacientes_id; ',str(row[4],'-fecha; ',str(row[5])))
    #         row = all.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return []
    

# Diagnósticos
@conexion_segura
def guardar_diagnostico(diagnostico) -> None:
    return None

def obtener_diagnostico_por_paciente(paciente) -> Diagnostico or None:
    return None

@conexion_segura
def obtener_diagnosticos() -> list[Diagnostico]:
    cursor = kwargs['cursor']

    # all = cursor.execute("SELECT * FROM medicos")
    # if all.rowcount > 0: 
    #     row = all.fetchone() 
    #     while row is not None:
    #         print('medicos_id :',str(row[1]), '-pacientes_id :', str(row[2]), '-enfermedad; ',str(row[3]))
    #         row = all.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return []