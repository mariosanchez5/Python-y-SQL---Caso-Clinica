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
    obtener_pacientes, obtener_medicos, obtener_habitaciones,\
    obtener_camas, obtener_examenes, obtener_diagnosticos,\
    obtener_habitacion_por_id, obtener_cama_por_id, obtener_examenes_por_paciente

# Agregar datos de prueba
def inicializar_datos():
    pacientes_a_agregar = [
        ("Juan", "Pérez", "11111111-1"),
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
        ("Mónica", "García", "5050505-5"),
        ("Andrés", "Fernández", "6060606-6"),
        ("María", "Ruiz", "7070707-7"),
        ("Juan", "González", "8080808-8"),
        ("Carolina", "Martínez", "9090909-9"),
        ("Pedro", "Rodríguez", "10101010-0")
    ]
    
    habitaciones_a_agregar = [ 'A', 'B', 'C', 'D', 'E',
                                'F', 'G', 'H', 'I', 'J']
    
    # Cada tupla contiene (id_cama, id_habitacion)
    camas_a_agregar = [(1, 2), (2, 0), (3, 4), (4, 1), (5, 3), (6, 0), (7, 2), (8, 1), (9, 4), (10, 0), 
                       (11, 3), (12, 2), (13, 1), (14, 0), (15, 4), (16, 3), (17, 2), (18, 1), (19, 0),
                       (20, 4), (21, 3), (22, 2), (23, 1), (24, 0), (25, 4), (26, 3), (27, 2), (28, 1),
                       (29, 0), (30, 4), (31, 3), (32, 2), (33, 1), (34, 0), (35, 4), (36, 3), (37, 2)
    ]

    def mensaje_error(funcion):
        print(f"El método {funcion} no está implementado, o está devolviendo None a todo evento.")
    
    print("Inicializando datos de prueba...")

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


    # Agregar médicos
    for medico in medicos_a_agregar:
        guardar_medico(
            Medico(
                nombre=medico[0], 
                apellido=medico[1], 
                rut=medico[2], 
                pacientes=[]
        ))
    
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
   
    # Los siguientes pacientes, uno a cada médico
    for i, paciente in enumerate(pacientes_a_agregar[4:]):
        medico = obtener_medico_por_rut(medicos_a_agregar[i+2][2])
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

    # Agregar habitaciones
    for habitacion in habitaciones_a_agregar:
        h = Habitacion(habitacion, [])
        guardar_habitacion(h)


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

    # Asignar camas a todos los pacientes
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

    # Agregar exámenes
    global contador_examenes
    contador_examenes = 0
    def generar_examen(paciente, nombre, resultado, prediagnostico):
        global contador_examenes
        contador_examenes += 1
        return Examen(
            id=contador_examenes,
            paciente=paciente.rut,
            nombre=nombre,
            resultado=resultado,
            medico=paciente.rut_medico_tratante,
            prediagnostico=prediagnostico
        )

    examenes_a_agregar = [
        # (índice paciente, prediagnóstico, nombre, resultado)
        (0, "Diabetes", "Examen de sangre", "Normal"),
        (5, "Intoxicación", "Examen de orina", "Anormal"),
        (7, "Infección", "Examen de sangre", "Anormal"),
        (9, "Gripe", "Examen de sangre", "Normal"),
        (2, "Gastritis", "Endoscopía", "Anormal"),
        (4, "Neumonía", "Radiografía", "Anormal"),
        (1, "Anemia", "Examen de sangre", "Anormal"),
        (6, "Covid-19", "PCR", "Normal"),
        (8, "Intoxicación", "Examen de orina", "Normal"),
        (3, "Gastritis", "Endoscopía", "Normal")
    ]
    # examenes_a_agregar = [
    #     # (índice, nombre, resultado, prediagnostico)
    #     (0, "Examen de sangre", "Normal", "Diabetes"),
    #     (5, "Examen de orina", "Anormal", "Intoxicación"),
    #     (7, "Examen de sangre", "Anormal", "Infección"),
    #     (9, "Examen de sangre", "Normal", "Gripe"),
    #     (2, "Endoscopía", "Anormal", "Gastritis"),
    #     (4, "Radiografía", "Anormal", "Neumonía"),
    #     (1, "Examen de sangre", "Anormal", "Anemia"),
    #     (6, "PCR", "Normal", "Covid-19"),
    #     (8, "Examen de orina", "Normal", "Intoxicación"),
    #     (3, "Endoscopía", "Normal", "Gastritis")

    # ]

    for examen in examenes_a_agregar:
        paciente = obtener_paciente_por_rut(pacientes_a_agregar[examen[0]][2])
        if paciente is None:
            mensaje_error("obtener_paciente_por_rut")
            break
        e = generar_examen(
            paciente = paciente,
            nombre = examen[2],
            resultado = examen[3],
            prediagnostico = examen[1]
        )
        print(e.to_dict())
        paciente.agregar_examen(e)
        guardar_examen(e)
        guardar_paciente(paciente)

    pacientes_con_examenes = obtener_pacientes()
    for paciente in pacientes_con_examenes:
        print(paciente.to_dict())
        print()
    
    input("Presione enter para continuar")

    global contador_diagnosticos
    contador_diagnosticos = 0
    
    def siguiente_diagnostico(examenes_por_revisar):
        global contador_diagnosticos
        contador_diagnosticos += 1
        anomalos = [ i for i in examenes_paciente if i.resultado == "Anormal" ]
        for e in anomalos:
            # Eliminar el examen actual de la lista de exámenes por revisar
            for r in examenes_por_revisar:
                if e.id == r.id:
                    examenes_por_revisar.remove(r)
                    break
            # Buscar exámenes relacionados con la enfermedad
            examenes_diagnostico = []
            enfermedad = e.prediagnostico
            for i in examenes_por_revisar:
                if i.prediagnostico == enfermedad:
                    examenes_diagnostico.append(i).id
                    examenes_por_revisar.remove(i)
            # Retornar diagnóstico: (id, enfermedad, [id_examenes])
            yield (contador_diagnosticos, enfermedad, examenes_diagnostico) 

    # Agregar diagnósticos
    for paciente in pacientes_a_agregar:
        p = obtener_paciente_por_rut(paciente[2])
        if p is None:
            mensaje_error("obtener_paciente_por_rut")
            break

        diagnosticos_paciente = []
        examenes_paciente = list(obtener_examenes_por_paciente(p))
        examenes_por_revisar = examenes_paciente.copy()
        for d in siguiente_diagnostico(examenes_por_revisar):
            diagnostico = Diagnostico(
                id=d[0],
                medico=p.rut_medico_tratante,
                enfermedad=d[1],
                paciente=p.rut,
                examenes=d[2]
            )
            diagnosticos_paciente.append(diagnostico)
            guardar_diagnostico(diagnostico)

        guardar_paciente(p)

    print("Datos de prueba inicializados!")
    print()
