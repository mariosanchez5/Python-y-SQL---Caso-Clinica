from src.repositorio_clinica import *
from src.inicializacion import *
from src.auxiliares import mostrar_menu, limpiar_pantalla

inicializar_datos()

###### AUXILIARES ######
def solicitar_cama_disponible_por_id():
    id_cama = int(input("Ingrese el ID de la cama: "))
    cama = obtener_cama_por_id(id_cama)
    if cama:
        if cama.disponible:
            return cama
    print("Cama no encontrada o no disponible") 
    return None


def solicitar_cama_por_id():
    id_cama = int(input("Ingrese el ID de la cama: "))
    cama = obtener_cama_por_id(id_cama)
    if cama:
        return cama
    print("Cama no encontrada")
    return None


def solicitar_habitacion_por_id():
    id_habitacion = input("Ingrese el ID de la habitación: ")
    habitacion = obtener_habitacion_por_id(id_habitacion)
    if habitacion:
        return habitacion
    print("Habitación no encontrada.")
    return None


def solicitar_paciente():
    rut = input("Ingrese el RUT del paciente sin puntos con guión: ")
    paciente = obtener_paciente_por_rut(rut)
    if not paciente:
        print("Paciente no registrado")
        return None
    return paciente


def solicitar_medico():
    rut = input("Ingrese el RUT del médico sin puntos con guión: ")
    medico = obtener_medico_por_rut(rut)
    if not medico:
        print("Médico no registrado")
        return None
    return medico

#########################


def mostrar_pacientes():
    pacientes = obtener_pacientes()
    for paciente in pacientes:
        print(paciente.to_dict())


def mostrar_paciente_por_rut():
    paciente = solicitar_paciente() 
    if paciente:
        print(paciente.to_dict())
    else:
        print("Paciente no encontrado")


def cambiar_paciente_cama():
    paciente = solicitar_paciente()
    if not paciente: return
    # Hasta acá se ha validado que el paciente existe
    cama_asignada = solicitar_cama_disponible_por_id()
    if not cama_asignada: return
    # Hasta acá se ha validado que el paciente existe y la cama está disponible
    if paciente.id_cama:
        cama_actual = obtener_cama_por_id(paciente.id_cama)
        cama_actual.desocupar()
        guardar_cama(cama_actual)
    paciente.asignar_cama(cama_asignada)
    cama_asignada.ocupar(paciente)
    guardar_paciente(paciente)
    guardar_cama(cama_asignada)
    print("Cama asignada correctamente")
    return


def cambiar_paciente_medico():
    paciente = solicitar_paciente()
    if not paciente: return
    medico = solicitar_medico()
    if not medico: return
    # Hasta acá se ha validado que el paciente y el médico existen
    if paciente.rut_medico_tratante:
        medico_actual = obtener_medico_por_rut(paciente.rut_medico_tratante)
        medico_actual.quitar_paciente(paciente)
        guardar_medico(medico_actual)
    paciente.asignar_medico(medico)
    medico.agregar_paciente(paciente)
    guardar_paciente(paciente)
    guardar_medico(medico)
    print("Médico asignado correctamente")
    return


def crear_cama():
    habitacion = solicitar_habitacion_por_id()
    if not habitacion: return
    camas = list(obtener_camas())
    cama = Cama(len(camas) + 1) # ID de cama correlativo
    cama.asignar_habitacion(habitacion)
    guardar_cama(cama)
    habitacion.agregar_cama(cama)
    guardar_habitacion(habitacion)
    print("Cama creada correctamente")
    return


def crear_habitacion():
    id_habitacion = input("Ingrese el ID de la habitación: ")
    if obtener_habitacion_por_id(id_habitacion):
        print("Habitación ya existe")
        return
    habitacion = Habitacion(id_habitacion, [])
    guardar_habitacion(habitacion)
    print("Habitación creada correctamente")


def cambiar_cama_habitacion():
    cama = solicitar_cama_por_id()
    if not cama: return
    print(f"La cama actualmente está en la habitación: {cama.id_habitacion}")
    print("Seleccione la habitación a la que desea mover la cama")
    habitacion_destino = solicitar_habitacion_por_id()
    if not habitacion_destino: return
    # Hasta acá se ha validado que la cama y la habitación existen
    habitacion_actual = obtener_habitacion_por_id(cama.id_habitacion)
    print(habitacion_actual.to_dict())
    habitacion_actual.quitar_cama(cama)
    guardar_habitacion(habitacion_actual)
    # Cama libre   
    cama.asignar_habitacion(habitacion_destino)
    habitacion_destino.agregar_cama(cama)
    if not cama.disponible:
        paciente = obtener_paciente_por_cama(cama)
        # Se reasigna la cama al paciente para actualizar la habitación
        paciente.asignar_cama(cama)
        guardar_paciente(paciente)
    guardar_habitacion(habitacion_destino)
    guardar_cama(cama)
    print("Cama asignada a habitación correctamente")
    return

def crear_camas_y_habitaciones():
    opciones_validas = ["Crear cama", "Mover cama", "Crear habitación", "Volver atrás"]
    while True:
        opcion = mostrar_menu(
            "Crear camas y habitaciones", 
            opciones_validas, 
            "Ingrese el número de la opción deseada: "
        )
        if opcion == "1":
            crear_cama()
            input("Presione enter para continuar")
        elif opcion == "2":
            cambiar_cama_habitacion()
            input("Presione enter para continuar")
        elif opcion == "3":
            crear_habitacion()
            input("Presione enter para continuar")
        elif opcion == "4":
            limpiar_pantalla()
            break
        else:
            print("Opción no válida")
            input("Presione enter para continuar")
    

def validar_rut(rut):
    rut = rut.replace(".", "")
    rut = rut.replace("-", "")
    if len(rut) < 8:
        return False
    try:
        int(rut[:-1])
    except:
        return False
    return True