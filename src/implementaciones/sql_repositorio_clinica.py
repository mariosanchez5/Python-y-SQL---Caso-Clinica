from src.paciente import Paciente
from src.habitacion import Habitacion
from src.examen import Examen
from src.medico import Medico
from src.diagnostico import Diagnostico
from src.cama import Cama
from src.config import leer_config
from src.auxiliares import rut_a_int, int_a_rut

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

@conexion_segura
def guardar_campos(tabla, datos, cursor=None):
    campos = datos.keys()
    valores = datos.values()
    campos_str = ', '.join(campos)
    valores_str = ', '.join(['%s'] * len(valores))
    # Asumir el primer campo como la llave primaria
    llave = list(campos)[0]
    # Buscar si ya existe
    cursor.execute(f"SELECT * FROM {tabla} WHERE {llave} = %s", (datos[llave],))
    if cursor.rowcount > 0:
        # Actualizar
        campos = [f"{campo} = %s" for campo in campos]
        campos_str = ', '.join(campos)
        cursor.execute(
            f"UPDATE {tabla} SET {campos_str} WHERE {llave} = %s",
            tuple(valores) + (datos[llave],)
        )
    else:
        # Insertar
        cursor.execute(
            f"INSERT INTO {tabla} ({campos_str}) VALUES ({valores_str})",
            tuple(valores)
        )


@conexion_segura
def borrar_fila(tabla, llave, valor, cursor=None):
    cursor.execute(f"DELETE FROM {tabla} WHERE {llave} = %s", (valor,))
########################################


# Pacientes
def guardar_paciente(paciente) -> None:
    guardar_campos(
        tabla = 'pacientes',
        datos = {
            'rut': rut_a_int(paciente.rut),
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'medicos_id': rut_a_int(paciente.rut_medico_tratante),
            'camas_id': paciente.id_cama
        }
    )

@conexion_segura
def quitar_paciente(paciente, cursor=None) -> None:
    borrar_fila('pacientes', 'rut', rut_a_int(paciente.rut))


@conexion_segura
def obtener_paciente_por_rut(rut, cursor=None) -> Paciente or None:
    rut_int = rut_a_int(rut)
    cursor.execute("SELECT * FROM pacientes WHERE rut = %s",(rut_int,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()

        rut_medico = None
        if row[3]:
            rut_medico = int_a_rut(row[3])
        
        paciente = Paciente(
            nombre=row[1],
            apellido=row[2],
            rut=int_a_rut(row[0]),
            medico_tratante=rut_medico,
            cama=row[4]
        )
        return paciente
    return None


@conexion_segura
def obtener_pacientes(cursor=None) -> list[Paciente]:
    cursor.execute("SELECT * FROM pacientes")
    for row in cursor:
        # Obtener médico tratante
        rut_medico = None
        if row[4]:
            medico = obtener_medico_por_rut(row[4])
            rut_medico = medico.rut if medico else None

        yield Paciente(
            nombre=row[1],
            apellido=row[2],
            rut=int_a_rut(row[0]),
            medico_tratante=rut_medico,
            cama=row[4]
        )
    return []


# Médicos
def guardar_medico(medico, cursor=None) -> None:
   guardar_campos(
        tabla = 'medicos',
        datos = {
            'rut': rut_a_int(medico.rut),
            'nombre': medico.nombre,
            'apellido': medico.apellido
        }
    )
 

def quitar_medico(medico, cursor=None) -> None:
    borrar_fila('medicos', 'rut', rut_a_int(medico.rut))


@conexion_segura
def obtener_medico_por_rut(rut, cursor=None) -> Medico or None:
    rut_int = rut_a_int(rut)
    cursor.execute("SELECT * FROM medicos WHERE rut = %s",(rut_int,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        rut, nombre, apellido = row
        return Medico(
            nombre=nombre,
            apellido=apellido,
            rut=int_a_rut(rut)
        )
    return None


@conexion_segura
def obtener_medicos(cursor=None) -> list[Medico]:
    cursor.execute("SELECT * FROM medicos")
    for row in cursor:
        rut, nombre, apellido = row
        yield Medico(
            nombre=nombre,
            apellido=apellido,
            rut=int_a_rut(rut)
        )
    return []


# Habitaciones
def guardar_habitacion(habitacion, cursor=None) -> None:
    guardar_campos(
        tabla = 'habitaciones',
        datos = {
            'id_habitacion': habitacion.id,
            'camas_ids': habitacion.id_camas
        }
    )


@conexion_segura
def obtener_habitacion_por_id(id, cursor=None) -> Habitacion or None:
    cursor.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s",(id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        return Habitacion(
            id = row[0], 
            id_camas = row[1]
        )
    return None


@conexion_segura
def obtener_habitaciones(cursor=None) -> list[Habitacion]:
    cursor.execute("SELECT * FROM habitaciones")
    for row in cursor:
        yield Habitacion(row[0])


# Camas
def guardar_cama(cama, cursor=None) -> None:
    guardar_campos(
        tabla = 'camas',
        datos = {
            'id_cama': cama.id,
            'disponible': cama.disponible,
            'habitaciones_id': cama.id_habitacion
        }
    )


@conexion_segura
def obtener_cama_por_id(id, cursor=None) -> Cama or None:
    cursor.execute("SELECT * FROM camas WHERE id_cama = %s",(id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        return Cama(row[0], row[1], row[2])
    return None


@conexion_segura
def obtener_camas() -> list[Cama]:
    cursor.execute("SELECT * FROM camas")
    for row in cursor:
        yield Cama(row[0], row[1], row[2])


@conexion_segura
def obtener_camas_disponibles() -> list[Cama]:
    cursor.execute("SELECT * FROM camas WHERE disponible = TRUE")
    for row in cursor:
        yield Cama(row[0], row[1], row[2])


# Exámenes
def guardar_examen(examen) -> int or None:
    guardar_campos(
        tabla = 'examenes',
        datos = {
            'id_examen': examen.id,
            'nombre': examen.nombre,
            'resultado': examen.resultado,
            'medicos_id': rut_a_int(examen.rut_medico),
            'pacientes_id': rut_a_int(examen.rut_paciente),
            'fecha': examen.fecha
        }
    )


@conexion_segura
def obtener_examen_por_id(id) -> Examen or None:
    cursor.execute("SELECT * FROM examenes WHERE id_examen = %s",(id,))
    if cursor.rowcount > 0:
        return Examen(row[0], row[1], row[2], int_to_rut(row[3]), int_to_rut(row[4]), row[5])
    return None


@conexion_segura
def obtener_examenes_por_paciente(paciente, cursor=None) -> list[Examen]:
    rut_paciente = rut_a_int(paciente.rut)
    cursor.execute("SELECT * FROM examenes WHERE pacientes_id = %s",(rut_paciente,))
    for row in cursor:
        yield Examen(row[0], row[1], row[2], int_to_rut(row[3]), int_to_rut(row[4]), row[5])   
    return []


@conexion_segura
def obtener_examenes(cursor=None) -> list[Examen]:
    cursor.execute("SELECT * FROM examenes")
    for row in cursor:
        yield Examen(row[0], row[1], row[2], int_to_rut(row[3]), int_to_rut(row[4]), row[5])
    return []
    

# Diagnósticos
def guardar_diagnostico(diagnostico, cursor=None) -> None:
    guardar_campos(
        tabla = 'diagnosticos',
        datos = {
            'id_diagnostico': diagnostico.id,
            'enfermedad': diagnostico.enfermedad,
            'medicos_id': rut_a_int(diagnostico.rut_medico),
            'pacientes_id': rut_a_int(diagnostico.rut_paciente),
            'id_examenes': diagnostico.id_examenes
        }
    )


def obtener_diagnostico_por_id(id, cursor=None) -> Diagnostico or None:
    cursor.execute("SELECT * FROM diagnosticos WHERE id = %s",(id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        return Diagnostico(
            id=row[0],
            rut_medico=int_to_rut(row[2]),
            enfermedad=row[3],
            rut_paciente=int_to_rut(row[1]),
            id_examenes=row[4]
        )
    return None


@conexion_segura
def obtener_diagnosticos_por_paciente(paciente, cursor=None) -> list[Diagnostico]:
    rut_paciente = rut_a_int(paciente.rut)
    cursor.execute("SELECT * FROM diagnosticos WHERE pacientes_id = %s",(rut_paciente,))
    if cursor.rowcount > 0:
        yield Diagnostico(
            id=row[0],
            rut_medico=int_to_rut(row[2]),
            enfermedad=row[3],
            rut_paciente=int_to_rut(row[1]),
            id_examenes=row[4]
        )
    return []


@conexion_segura
def obtener_diagnosticos(cursor=None) -> list[Diagnostico]:
    cursor.execute("SELECT * FROM diagnosticos")
    for row in cursor:
        yield Diagnostico(
            id=row[0],
            rut_medico=int_to_rut(row[2]),
            enfermedad=row[3],
            rut_paciente=int_to_rut(row[1]),
            id_examenes=row[4]
        )
    return []