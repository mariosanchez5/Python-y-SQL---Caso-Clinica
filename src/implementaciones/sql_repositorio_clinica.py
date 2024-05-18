from src.paciente import Paciente
from src.habitacion import Habitacion
from src.examen import Examen
from src.medico import Medico
from src.diagnostico import Diagnostico
from src.cama import Cama
from src.config import leer_config
from src.auxiliares import rut_to_int, int_to_rut

import os

import psycopg2
import psycopg2.extensions as extensions

########################
# Gestión de la conexión
conexion = None
db_config = leer_config()['sql']

def obtener_schemas():
    schemas_limpios = []
    schemas_dir = db_config['schemas_dir']
    # Verificar si el directorio de schemas existe
    # Si la ruta es relativa, convertirla a absoluta
    schemas_dir = os.path.abspath(schemas_dir)
    if not os.path.exists(schemas_dir):
        raise FileNotFoundError(f"El directorio de schemas {schemas_dir} no existe")
    # Leer los archivos de schemas
    for schema in db_config['schemas']:
        # Verificar si el archivo existe
        schema_file = os.path.join(schemas_dir, schema)
        # Si no tiene la extensión .sql, agregarla
        if not schema_file.endswith('.sql'):
            schema_file += '.sql'
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"El archivo de schema {schema_file} no existe")
        schemas_limpios.append(schema_file)
    return schemas_limpios


def obtener_conexion():
    global conexion
    conn_config = db_config['conexion']
    if conexion is None:
        conexion = psycopg2.connect(
            **conn_config,
        )
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


def verificar_db_existente():
    host = db_config['conexion']['host']
    port = db_config['conexion']['port']
    dbname = db_config['conexion']['dbname']
    user = db_config['conexion']['user']
    password = db_config['conexion']['password']
    # Verificar que la db exista
    conexion = psycopg2.connect(
        host=host,
        port=port,
        dbname='postgres',
        user=user,
        password=password
    )
    cursor = conexion.cursor()
    conexion.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    if cursor.fetchone():
        # Si existe, borrarla
        cursor.execute(f"DROP DATABASE {dbname}")
    cursor.execute(f"CREATE DATABASE {dbname}")
    conexion.commit()
    conexion.close()

@conexion_segura
def cargar_schemas(cursor=None):
    # Cargar los schemas
    schemas = obtener_schemas()
    for schema in schemas:
        with open(schema) as f:
            cursor.execute(f.read())

verificar_db_existente()
cargar_schemas()

########################################


# Pacientes
@conexion_segura
def guardar_paciente(paciente, cursor=None) -> None:
    p = obtener_paciente_por_rut(paciente.rut)
    if p:
        cursor.execute("DELETE FROM pacientes WHERE rut = %s", (p.rut,))
    # Conseguir datos necesarios 
    rut_paciente = rut_to_int(paciente.rut)
    
    # Obtener id del médico tratante
    if paciente.medico_tratante:
        cursor.execute(
            "SELECT id FROM medicos WHERE rut = %s",
            (rut_to_int(paciente.medico_tratante.rut),)
        )
    id_medico = cursor.fetchone()[0]
    # Obtener id de la cama

    
    fila_nueva = (
        paciente.nombre,
        paciente.apellido,
        rut_paciente,
        rut_to_int(paciente.medico_tratante.rut) if paciente.medico_tratante else None,
        paciente.cama.id if paciente.cama else None
    )
    cursor.execute(
        "INSERT INTO pacientes (nombre, apellido, rut) VALUES (%s, %s, %s, %s, %s)",
        fila_nueva
    )
@conexion_segura
def quitar_paciente(paciente, cursor=None) -> None:
    return None


@conexion_segura
def obtener_paciente_por_rut(rut, cursor=None) -> Paciente or None:
    #select_filter_paciente = cursor.execute("SELECT * FROM pacientes WHERE rut = %s",(rut,))
    return None


@conexion_segura
def obtener_pacientes(cursor=None) -> list[Paciente]:
    all = cursor.execute("SELECT * FROM pacientes")
    for row in all:
        nombre, apellido, rut, rut_medico_tratante, id_cama = row
        medico = obtener_medico_por_rut(rut_medico_tratante)
        cama = obtener_cama_por_id(cama)
        paciente = Paciente(nombre, apellido, rut, medico, cama)
    return []


# Médicos
@conexion_segura
def guardar_medico(medico, cursor=None) -> None:
    # m = obtener_medico_por_rut(medico.rut)
    # if m:
    #     cursor.execute("DELETE FROM medicos WHERE rut = %s", (m,))
    # cursor.execute("INSERT INTO medicos (nombre, apellido, rut) VALUES (%s, %s, %s)", (medico.nombre, medico.apellido, medico.rut))
    return None
    

@conexion_segura
def quitar_medico(medico, cursor=None) -> None:
    m = obtener_medico_por_rut(medico.rut)
    if m:
        cursor.execute("DELETE FROM medicos WHERE rut = %s", (m,))
    return None

@conexion_segura
def obtener_medico_por_rut(rut, cursor=None) -> Medico or None:
    resultado = cursor.execute("SELECT * FROM medicos WHERE rut = %s",(rut,))
    if resultado.rowcount > 0:
        row = resultado.fetchone()
        nombre, apellido, rut = row
        return Medico(nombre, apellido, rut)


@conexion_segura
def obtener_medicos(cursor=None) -> list[Medico]:
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
def guardar_habitacion(habitacion, cursor=None) -> None:
    # h = obtener_habitacion_por_id(habitacion.id)
    # if h:
    #     cursor.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (h,))
    # cursor.execute("INSERT INTO habitaciones (id_habitacion) VALUES (%s)", (habitacion.id))
    return None


@conexion_segura
def obtener_habitacion_por_id(id, cursor=None) -> Habitacion or None:
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
def obtener_habitaciones(cursor=None):
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
def obtener_cama_por_id(id, cursor=None) -> Cama or None:
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


def obtener_examenes_por_paciente(paciente, cursor=None) -> list[Examen]:
    return []

@conexion_segura
def obtener_examenes(cursor=None) -> list[Examen]:
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
def guardar_diagnostico(diagnostico, cursor=None) -> None:
    return None

def obtener_diagnostico_por_paciente(paciente, cursor=None) -> Diagnostico or None:
    return None

@conexion_segura
def obtener_diagnosticos(cursor=None) -> list[Diagnostico]:
    # all = cursor.execute("SELECT * FROM medicos")
    # if all.rowcount > 0: 
    #     row = all.fetchone() 
    #     while row is not None:
    #         print('medicos_id :',str(row[1]), '-pacientes_id :', str(row[2]), '-enfermedad; ',str(row[3]))
    #         row = all.fetchone()
    # else:
    #     print('No existen registros en la base de datos')
    return []