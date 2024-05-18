import psycopg2
import config

conexion = None

def ObtenerConexion():
    if conexion is None:
        conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    return conexion    


def OperacionSegura(func):
    def wrapper(*args, **kwargs):
        try:
            conexion = ObtenerConexion()
            cursor = conexion.cursor()
            func(*args, **kwargs)
            conexion.commit()
            conexion.close()
        except Exception as e:
            print(f"Error: {e}")
    return wrapper


def VerTodosPacientes():
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    all_pacientes = cursor.execute("SELECT * FROM Pacientes")
    if all_pacientes.rowcount > 0: 
        row = all_pacientes.fetchone() 
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-Edad:',str(row[4]),'-Genero:',str(row[5]))
            row = all_pacientes.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()

@OperacionSegura
def VerTodosPacientes2():
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    all_pacientes = cursor.execute("SELECT * FROM Pacientes")
    if all_pacientes.rowcount > 0: 
        row = all_pacientes.fetchone() 
        while row is not None:
            Paciente.FromRow(row).ImprimirPaciente()
            #print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-Edad:',str(row[4]),'-Genero:',str(row[5]))
            row = all_pacientes.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()

def FiltrarPacientes(search):
    conexion = obtenerConexion()
    cursor = conexion.cursor()

    select_filter_paciente = cursor.execute("SELECT * FROM Pacientes WHERE rut = %s",(search,))
    if select_filter_paciente.rowcount > 0:
        row = select_filter_paciente.fetchone()
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-Edad:',str(row[4]),'-Genero:',str(row[5]))
            row = select_filter_paciente.fetchone()
    else:
        print('No existen registros en la base de datos')

    conexion.close()

def CambiarPacienteCama(id_nueva_cama, id_paciente):
    conexion = ObtenerConexion()

    cursor = conexion.cursor() 
    cursor.execute("UPDATE asignacioncama SET id_cama = %s WHERE id_paciente = %s", (id_nueva_cama, id_paciente))
    conexion.commit()
    print("Cambio de cama realizado con éxito.")
    conexion.close()

def CambiarMedicoPaciente(id_nuevo_medico,id_paciente):
    conexion = ObtenerConexion()

    cursor = conexion.cursor() 
    cursor.execute("UPDATE asignacionmedico SET id_medico = %s WHERE id_paciente = %s", (id_nuevo_medico, id_paciente))
    conexion.commit()
    print("Cambio de Medico realizado con éxito.")
    conexion.close()

def CrearCamas(ncamas, disponible=True):
    conexion = ObtenerConexion()

    cursor = conexion.cursor() 
    for _ in range(ncamas):
        cursor.execute("INSERT INTO cama (disponible) VALUES (%s)", (disponible,))
    conexion.commit()
    print(f"{ncamas} camas creadas con éxito.")
    conexion.close()

def CrearHabitaciones(ncamas,zona ):
    conexion = ObtenerConexion()
    cursor = conexion.cursor() 
    cursor.execute("INSERT INTO habitacion (zona, ncamas) VALUES (%s, %s)", (zona, ncamas))
    conexion.commit()
    print("Habitación creada con éxito.")
    conexion.close()