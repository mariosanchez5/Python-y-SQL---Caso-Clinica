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

def CambiarPacienteCama():
    pass

def CambiarMedicoPaciente():
    pass

def CrearCamas():
    pass

def CrearHabitaciones():
    pass