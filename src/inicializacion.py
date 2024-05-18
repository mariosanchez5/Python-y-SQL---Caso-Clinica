from src.paciente import Paciente
from src.medico import Medico
from src.habitacion import Habitacion
from src.cama import Cama
from src.examen import Examen
from src.diagnostico import Diagnostico

from src.repositorio_clinica import \
    guardar_paciente, guardar_medico, guardar_habitacion,\
    guardar_cama, guardar_examen, guardar_diagnostico,\
    obtener_paciente_por_rut, obtener_medico_por_rut,\
    obtener_habitacion_por_id, obtener_cama_por_id,\
    obtener_examen_por_id, obtener_diagnostico_por_id,\
    obtener_pacientes, obtener_medicos, obtener_habitaciones,\
    obtener_camas, obtener_examenes, obtener_diagnosticos

# Agregar datos de prueba
def inicializar_datos():
    pacientes_a_agregar = [
        ("Juan", "Pérez", "1111111-1"),
        ("María", "Gómez", "2222222-2"),
        ("Pedro", "Rodríguez", "3333333-3"),
        ("Ana", "Martínez", "4444444-4"),
        ("Laura", "Sánchez", "5555555-5"),
        ("Carlos", "López", "6666666-6"),
        ("Sofía", "García", "7777777-7"),
        ("Diego", "Fernández", "8888888-8"),
        ("Paula", "Ruiz", "9999999-9"),
        ("Miguel", "González", "10101010-0")
    ]
    
    medicos_a_agregar = [
        ("Marcela", "González", "1010101-1"),
        ("Felipe", "Martínez", "2020202-2"),
        ("Carmen", "Rodríguez", "3030303-3"),
        ("Jorge", "López", "4040404-4"),
        ("Mónica", "García", "5050505-5")
    ]
    
    habitaciones_a_agregar = [ 'A', 'B', 'C', 'D', 'E' ]
    
    # Cada tupla contiene (id_cama, id_habitacion)
    camas_a_agregar = [(1, 2), (2, 0), (3, 4), (4, 1), (5, 3), (6, 0), (7, 2), (8, 1), (9, 4), (10, 0), 
                       (11, 3), (12, 2), (13, 1), (14, 0), (15, 4), (16, 3), (17, 2), (18, 1), (19, 0), 
                       (20, 4), (21, 3), (22, 2), (23, 1), (24, 0), (25, 4), (26, 3)
    ]

    def mensaje_error(funcion):
        print(f"El método {funcion} no está implementado, o está devolviendo None a todo evento.")
    
    print("Inicializando datos de prueba...")
    print("Agregando pacientes...")
    # Agregar pacientes
    for paciente in pacientes_a_agregar:
        paciente_a_agregar = {
            'nombre': paciente[0],
            'apellido': paciente[1],
            'rut': paciente[2],
            'medico_tratante': None,
            'cama': None,
            'diagnosticos': [],
            'examenes': [],
            'ultimo_examen': None
        }
        guardar_paciente(Paciente(**paciente_a_agregar))

    # Testear si se agregaron correctamente
    pacientes_agregados = obtener_pacientes()
    for paciente in pacientes_agregados:
        print(paciente.to_dict())

    input("Presione enter para continuar")


    print("Agregando médicos...")
    # Agregar médicos
    for medico in medicos_a_agregar:
        guardar_medico(Medico(*medico))

    # Testear si se agregaron correctamente
    medicos_agregados = obtener_medicos()
    for medico in medicos_agregados:
        print(medico.to_dict())
    
    input("Presione enter para continuar")

    print("Asignando algunos médicos a pacientes...")
    # Asignar algunos pacientes a médicos
    # Los primeros 2 pacientes al primer médico
    medico = obtener_medico_por_rut(medicos_a_agregar[0][2])
    for paciente in pacientes_a_agregar[:2]:
        if medico is None:
            mensaje_error("obtener_medico_por_rut")
            break
        p = obtener_paciente_por_rut(paciente[2])
        if p:
            p.asignar_medico(medico)
            medico.agregar_paciente(p)
            guardar_paciente(p)
            guardar_medico(medico)
        else:
            mensaje_error("obtener_paciente_por_rut")
            break
    # Los siguientes 2 pacientes al segundo médico
    medico = obtener_medico_por_rut(medicos_a_agregar[1][2])
    for paciente in pacientes_a_agregar[2:4]:
        if medico is None:
            mensaje_error("obtener_medico_por_rut")
            break
        p = obtener_paciente_por_rut(paciente[2])
        if p:
            p.asignar_medico(medico)
            medico.agregar_paciente(p)
            guardar_paciente(p)
            guardar_medico(medico)
        else:
            mensaje_error("obtener_paciente_por_rut")
            break

    print("Agregando habitaciones...")    
    # Agregar habitaciones
    for habitacion in habitaciones_a_agregar:
        h = Habitacion(habitacion, [])
        guardar_habitacion(Habitacion(habitacion))

    print("Agregando camas...")
    # Crear camas y agregar seudoaleatoriamente a las habitaciones
    for cama in camas_a_agregar:
        c = Cama(cama[0])
        hab = obtener_habitacion_por_id(habitaciones_a_agregar[cama[1]])
        if hab is None:
            mensaje_error("obtener_habitacion_por_id")
            break
        c.asignar_habitacion(hab)
        hab.agregar_cama(c)
        guardar_cama(c)
        guardar_habitacion(hab)

    print("Asignando camas a pacientes...")
    # Asignar camas a pacientes
    for i, paciente in enumerate(pacientes_a_agregar):
        p = obtener_paciente_por_rut(paciente[2])
        if p is None:
            mensaje_error("obtener_paciente_por_rut")
            break
        c = obtener_cama_por_id(i+1)
        if c is None:
            mensaje_error("obtener_cama_por_id")
            break
        p.asignar_cama(c)
        c.ocupar(p)
        guardar_paciente(p)
        guardar_cama(c)