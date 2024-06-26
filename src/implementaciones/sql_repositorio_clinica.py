from src.paciente import Paciente
from src.habitacion import Habitacion
from src.examen import Examen
from src.medico import Medico
from src.diagnostico import Diagnostico
from src.cama import Cama
from src.config import leer_config
from src.auxiliares import rut_a_int, int_a_rut, eliminar_puntos_guiones_a_entero

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
    campos = list(datos.keys())
    valores = list(datos.values())
    campos_str = ', '.join(campos)
    valores_str = ', '.join(['%s'] * len(valores))
    # Asumir el primer campo como la llave primaria
    llave = campos[0]
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
def obtener_ultimo_examen_por_rut_paciente(rut, cursor=None) -> Examen:
    rut_int = rut_a_int(rut)
    cursor.execute(f"SELECT * FROM examenes JOIN pacientes ON pacientes_id = pacientes.rut WHERE pacientes_id = {rut_int} ORDER BY examenes.fecha DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return Examen(
            id=row[0],
            nombre=row[1],
            resultado=row[2],
            prediagnostico=row[3],
            medico=row[4],
            paciente=row[5],
            fecha=row[6]
        )
    return None


@conexion_segura
def obtener_examenes_por_rut_paciente(rut, cursor=None) -> list[Examen]:
    rut_int = rut_a_int(rut)
    cursor.execute(f"SELECT * FROM examenes where pacientes_id = {rut_int}")
    for row in cursor:
        yield Examen(
            id=row[0],
            nombre=row[1],
            resultado=row[2],
            prediagnostico=row[3],
            medico=row[4],
            paciente=row[5],
            fecha=row[6]
        )
    return []

@conexion_segura
def obtener_paciente_por_rut(rut, cursor=None) -> Paciente or None:
    rut_int = rut_a_int(rut)
    examen_obtenido = obtener_ultimo_examen_por_rut_paciente(rut)
    examenes = [e.id for e in obtener_examenes_por_rut_paciente(rut)]
    cursor.execute("SELECT * FROM pacientes WHERE rut = %s",(rut_int,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()

        rut_medico = None
        if row[3]:
            rut_medico = int_a_rut(row[3])

        # Si no hay examen, se asigna None
        examen = None
        if examen_obtenido:
            examen = examen_obtenido.id
        
        paciente = Paciente(
            nombre=row[1],
            apellido=row[2],
            rut=int_a_rut(row[0]),
            medico_tratante=rut_medico,
            cama=obtener_cama_por_id(row[4]),
            examenes=examenes,
            ultimo_examen=examen
        )
        
        return paciente
    return None


@conexion_segura
def obtener_pacientes(cursor=None) -> list[Paciente]:
    diags = [(d.id, d.rut_paciente) for d in obtener_diagnosticos()]
    paciente_diags = { d[1]: [d[0]] for d in diags }
    cursor.execute("""
                SELECT pacientes.rut,pacientes.nombre,pacientes.apellido,pacientes.medicos_id,pacientes.camas_id,
                ARRAY_AGG(examenes.id_examen ORDER BY examenes.fecha DESC) AS examenes_agrupados,
                ARRAY_AGG(camas.habitaciones_id) AS habitaciones_agrupadas
                FROM pacientes JOIN camas ON camas_id = camas.id_cama 
                JOIN examenes ON rut = examenes.pacientes_id
                GROUP BY pacientes.rut
                """ )
    for row in cursor:
        # Obtener médico tratante
        rut_medico = None
        if row[3]:
            rut_medico = int_a_rut(row[3])
        paciente = Paciente(
            nombre=row[1],
            apellido=row[2],
            rut=int_a_rut(row[0]),
            medico_tratante=rut_medico,
            cama=obtener_cama_por_id(row[4]),
            examenes=row[5],
            ultimo_examen=max(row[5]),
            diagnosticos=paciente_diags.get(int_a_rut(row[0]), [])
        )
        yield paciente
    return []


# Médicos
def guardar_medico(medico) -> None:
   guardar_campos(
        tabla = 'medicos',
        datos = {
            'rut': rut_a_int(medico.rut),
            'nombre': medico.nombre,
            'apellido': medico.apellido
        }
    )
 

def quitar_medico(medico) -> None:
    borrar_fila('medicos', 'rut', rut_a_int(medico.rut))


@conexion_segura
def obtener_pacientes_por_rut_medico(rut_medico, cursor=None) -> list[Paciente]:
    medicos_id = rut_a_int(rut_medico)
    cursor.execute("SELECT * FROM pacientes WHERE medicos_id = %s",(medicos_id,))
    for row in cursor:
        rut, nombre, apellido, _ , camas_id = row
        yield Paciente(
            nombre=nombre,
            apellido=apellido,
            rut=int_a_rut(rut),
            medico_tratante=rut_medico,
            cama=obtener_cama_por_id(camas_id)
        )
    return []


@conexion_segura
def obtener_medico_por_rut(rut, cursor=None) -> Medico or None:
    rut_int = rut_a_int(rut)
    pacientes = [ p.rut for p in obtener_pacientes_por_rut_medico(rut) ]
    cursor.execute("SELECT * FROM medicos WHERE rut = %s",(rut_int,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        rut, nombre, apellido = row
        
        return Medico(
            nombre=nombre,
            apellido=apellido,
            rut=int_a_rut(rut),
            pacientes=pacientes
        )
    return None


@conexion_segura
def obtener_medicos(cursor=None) -> list[Medico]:
    cursor.execute("SELECT * FROM medicos")
    for row in cursor:
        rut, nombre, apellido = row
        rut_real = int_a_rut(rut)
        pacientes = [ p.rut for p in obtener_pacientes_por_rut_medico(rut_real) ]
        
        yield(
            Medico(
                nombre=nombre,
                apellido=apellido,
                rut=int_a_rut(rut),
                pacientes=pacientes
            )
        )
    return []


# Habitaciones
def guardar_habitacion(habitacion, cursor=None) -> None:
    guardar_campos(
        tabla = 'habitaciones',
        datos = {
            'id_habitacion': habitacion.id,
        }
    )


@conexion_segura
def obtener_camas_por_habitacion(habitacion, cursor=None) -> list[Cama]:
    cursor.execute("SELECT * FROM camas WHERE habitaciones_id = %s",(habitacion.id,))
    for row in cursor:
        yield Cama(row[0], row[1], row[2])


@conexion_segura
def obtener_habitacion_por_id(id, cursor=None) -> Habitacion or None:
    cursor.execute("SELECT * FROM habitaciones WHERE id_habitacion = %s",(id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        id = row[0]
        hab = Habitacion(id)
        camas = list(obtener_camas_por_habitacion(hab))
        camas = [cama.id for cama in camas]
        hab.id_camas = camas
        return hab
    return None


@conexion_segura
def obtener_habitaciones(cursor=None) -> list[Habitacion]:
    cursor.execute("SELECT * FROM habitaciones")
    for row in cursor:
        id = row[0]
        hab = Habitacion(id)
        camas = list(obtener_camas_por_habitacion(hab))
        camas = [cama.id for cama in camas]
        hab.id_camas = camas

        yield hab


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
def obtener_camas(cursor=None) -> list[Cama]:
    cursor.execute("SELECT * FROM camas")
    for row in cursor:
        yield Cama(row[0], row[1], row[2])


@conexion_segura
def obtener_camas_disponibles(cursor=None) -> list[Cama]:
    cursor.execute("SELECT * FROM camas WHERE disponible = TRUE")
    for row in cursor:
        yield Cama(row[0], row[1], row[2])

@conexion_segura
def obtener_paciente_por_cama(cama, cursor=None) -> Paciente or None:
    cursor.execute("SELECT * FROM pacientes WHERE camas_id = %s",(cama.id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        rut, nombre, apellido, medicos_id, camas_id = row
        return Paciente(
            nombre=nombre,
            apellido=apellido,
            rut=int_a_rut(rut),
            medico_tratante=int_a_rut(medicos_id),
            cama=cama
        )
    return None

# Exámenes
def guardar_examen(examen) -> int or None:
    guardar_campos(
        tabla = 'examenes',
        datos = {
            'id_examen': examen.id,
            'nombre': examen.nombre,
            'resultado': examen.resultado,
            'prediagnostico': examen.prediagnostico,
            'medicos_id': rut_a_int(examen.rut_medico),
            'pacientes_id': rut_a_int(examen.rut_paciente),
            'fecha': examen.fecha
        }
    )


@conexion_segura
def obtener_examen_por_id(id, cursor=None) -> Examen or None:
    cursor.execute("SELECT * FROM examenes WHERE id_examen = %s",(id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        return Examen(
            id=row[0],
            nombre=row[1],
            resultado=row[2],
            prediagnostico=row[3],
            medico=row[4],
            paciente=int_a_rut(row[5]),
            fecha=row[6]
        )  
    return None


@conexion_segura
def obtener_examenes_por_paciente(paciente, cursor=None) -> list[Examen]:
    rut_paciente = rut_a_int(paciente.rut)
    cursor.execute("SELECT * FROM examenes WHERE pacientes_id = %s",(rut_paciente,))
    for row in cursor:
        yield Examen(
            id=row[0],
            nombre=row[1],
            resultado=row[2],
            prediagnostico=row[3],
            medico=int_a_rut(row[4]),
            paciente=int_a_rut(row[5]),
            fecha=row[6]
        )   
    return []


@conexion_segura
def obtener_examenes(cursor=None) -> list[Examen]:
    cursor.execute("SELECT * FROM examenes")
    for row in cursor:
        yield Examen(
            id=row[0],
            nombre=row[1],
            resultado=row[2],
            prediagnostico=row[3],
            medico=int_a_rut(row[4]),
            paciente=int_a_rut(row[5]),
            fecha=row[6]
        )  
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
            'examenes_id': diagnostico.id_examenes
        }
    )

@conexion_segura
def obtener_diagnostico_por_id(id, cursor=None) -> Diagnostico or None:
    cursor.execute("SELECT * FROM diagnosticos WHERE id = %s",(id,))
    if cursor.rowcount > 0:
        row = cursor.fetchone()
        return Diagnostico(
            id=row[0],
            medico=int_a_rut(row[2]),
            enfermedad=row[3],
            paciente=int_a_rut(row[1]),
            examenes=row[4]
        )
    return None


@conexion_segura
def obtener_diagnosticos_por_paciente(paciente, cursor=None) -> list[Diagnostico]:
    rut_paciente = rut_a_int(paciente.rut)
    cursor.execute("SELECT * FROM diagnosticos WHERE pacientes_id = %s",(rut_paciente,))
    if cursor.rowcount > 0:
        for row in cursor:
            yield Diagnostico(
                id=row[0],
                paciente=int_a_rut(row[1]),
                medico=int_a_rut(row[2]),
                enfermedad=row[3],
                examenes=row[4]
            )
    yield []


@conexion_segura
def obtener_diagnosticos(cursor=None) -> list[Diagnostico]:
    cursor.execute("SELECT * FROM diagnosticos")
    for row in cursor:
        yield Diagnostico(
            id=row[0],
            paciente=int_a_rut(row[1]),
            medico=int_a_rut(row[2]),
            enfermedad=row[3],
            examenes=row[4]
        )
    return []