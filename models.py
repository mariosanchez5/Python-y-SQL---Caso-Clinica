import psycopg2
import config

def VerTodosPacientes():
    conexion = psycopg2.connect(host=config.host, database=config.database, user = config.user, password = config.password)   
    all_pacientes = conexion.cursor()

    all_pacientes.execute("SELECT * FROM Pacientes")
    if all_pacientes.rowcount > 0: 
        row = all_pacientes.fetchone() 
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-Edad:',str(row[4]),'-Genero:',str(row[5]))
            row = all_pacientes.fetchone()
    else:
        print('No existen registros en la base de datos')
    conexion.close()

def FiltrarPacientes(search):
    conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    select_filter_paciente = conexion.cursor() 
    
    select_filter_paciente.execute("SELECT * FROM Pacientes WHERE rut = %s",(search,))
    if select_filter_paciente.rowcount > 0:
        row = select_filter_paciente.fetchone()
        while row is not None:
            print('Nombre :',str(row[1]), '-Apellido :', str(row[2]), '-Rut; ',str(row[3]),'-Edad:',str(row[4]),'-Genero:',str(row[5]))
            row = select_filter_paciente.fetchone()
    else:
        print('No existen registros en la base de datos')

    conexion.close()

def CambiarPacienteCama(id_nueva_cama, id_paciente):
    conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    cursor = conexion.cursor() 
    cursor.execute("UPDATE asignacioncama SET id_cama = %s WHERE id_paciente = %s", (id_nueva_cama, id_paciente))
    conexion.commit()
    print("Cambio de cama realizado con éxito.")
    conexion.close()

def CambiarMedicoPaciente(id_nuevo_medico,id_paciente):
    conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    cursor = conexion.cursor() 
    cursor.execute("UPDATE asignacionmedico SET id_medico = %s WHERE id_paciente = %s", (id_nuevo_medico, id_paciente))
    conexion.commit()
    print("Cambio de Medico realizado con éxito.")
    conexion.close()

def CrearCamas(ncamas, disponible=True):
    conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    cursor = conexion.cursor() 
    for _ in range(ncamas):
        cursor.execute("INSERT INTO cama (disponible) VALUES (%s)", (disponible,))
    conexion.commit()
    print(f"{ncamas} camas creadas con éxito.")
    conexion.close()

def CrearHabitaciones(ncamas,zona ):
    conexion = psycopg2.connect(host=config.host,database=config.database,user=config.user,password=config.password)
    cursor = conexion.cursor() 
    cursor.execute("INSERT INTO habitacion (zona, ncamas) VALUES (%s, %s)", (zona, ncamas))
    conexion.commit()
    print("Habitación creada con éxito.")
    conexion.close()