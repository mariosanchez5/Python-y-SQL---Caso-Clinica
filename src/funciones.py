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
    print("-" * 40)
    print("Listado de pacientes")
    print("-" * 40)
    try:
        pacientes = obtener_pacientes()
        for paciente in pacientes:
            detalles_pacientes = paciente.to_dict()
            print(f"Nombre:          {detalles_pacientes['nombre']} {detalles_pacientes['apellido'] or 'Sin registro'}")
            print(f"RUT:             {detalles_pacientes['rut'] or 'Sin registro'}")
            print(f"Médico Tratante: {detalles_pacientes['medico_tratante'] or 'Sin registro'}")
            print(f"Cama:            {detalles_pacientes['cama'] or 'Sin registro'}")
            print(f"Habitación:      {detalles_pacientes['habitacion'] or 'Sin registro'}")
            print(f"Diagnósticos:    {detalles_pacientes['diagnosticos'] or 'Sin registro'}")
            print(f"Exámenes:        {detalles_pacientes['examenes'] or 'Sin registro'}")
            print(f"Último Examen:   {detalles_pacientes['ultimo_examen'] or 'Sin registro'}")
            print("-" * 40)
    except Exception as e:
        print(f"Error al obtener o mostrar pacientes: {e}")

#Versón anterior
def mostrar_pacientes_0():
    pacientes = obtener_pacientes()
    for paciente in pacientes:
        print(paciente.to_dict())


def mostrar_paciente_por_rut():
    print("-" * 40)
    print("Pacientes solicitado")
    print("-" * 40)
    paciente = solicitar_paciente()
    if paciente:
        detalles = paciente.to_dict()
        print(f"Nombre:          {detalles['nombre'] or 'Sin registro'}")
        print(f"Apellido:        {detalles['apellido'] or 'Sin registro'}")
        print(f"RUT:             {detalles['rut'] or 'Sin registro'}")
        print(f"Médico Tratante: {detalles['medico_tratante'] or 'Sin registro'}")
        print(f"Cama:            {detalles['cama'] or 'Sin registro'}")
        print(f"Habitación:      {detalles['habitacion'] or 'Sin registro'}")
        print(f"Diagnósticos:    {detalles['diagnosticos'] or 'Sin registro'}")
        print(f"Exámenes:        {detalles['examenes'] or 'Sin registro'}")
        print(f"Último Examen:   {detalles['ultimo_examen'] or 'Sin registro'}")
    else:
        print("Paciente no encontrado")

#Versión anterior
def mostrar_paciente_por_rut_0():
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

def mostrar_medicos():
    print("-" * 40)
    print("Listado de médicos")	
    print("-" * 40)
    try:
        medicos = obtener_medicos()
        for medicos in medicos:
            detalles = medicos.to_dict()
            print(f"Nombre:          {detalles['nombre']} {detalles['apellido'] or 'Sin registro'}")
            print(f"RUT:             {detalles['rut'] or 'Sin registro'}")
            print(f"Rut pacientes:   {detalles['rut_pacientes'] or 'Sin registros'}")
            print("-" * 40)
    except Exception as e:
        print(f"Error al obtener o mostrar medicos: {e}")

def mostrar_camas():
  print("-" * 40)
  print("Listado de camas")
  print("-" * 40)
  try:
    camas = obtener_camas()
    for cama in camas:
      detalles = cama.to_dict()
      estado_str = "Disponible" if detalles['disponible'] else "Ocupada"
      print(f"Cama:      {detalles['id'] or 'Sin registro'}")
      print(f"Estado:    {estado_str}")
      print(f"Habitación:{detalles['habitacion'] or 'Sin registros'}")
      print("-" * 40)
  except Exception as e:
    print(f"Error al obtener o mostrar camas: {e}")
    
def mostrar_habitaciones():
  print("-" * 40)
  print("Listado de habitaciones")
  print("-" * 40)
  try:
    habitaciones = obtener_habitaciones()
    for habitacion in habitaciones:
      detalles = habitacion.to_dict()
      print(f"Habitacion:    {detalles['id'] or 'Sin registro'}")
      print(f"Camas:         {detalles['camas'] or 'Sin registros'}")
      print("-" * 40)
  except Exception as e:
    print(f"Error al obtener o mostrar habitaciones: {e}")

def mostrar_habitaciones():
    print("-" * 40)
    print("Listado de habitaciones")
    print("-" * 40)
    try:
        habitaciones = obtener_habitaciones()
        
        # Ordenar las habitaciones por el campo 'id'
        habitaciones_ordenadas = sorted(habitaciones, key=lambda x: x.id)

        for habitacion in habitaciones_ordenadas:
            detalles = habitacion.to_dict()
            print(f"Habitacion:    {detalles['id'] or 'Sin registro'}")
            print(f"Camas:         {detalles['camas'] or 'Sin registros'}")
            print("-" * 40)
    except Exception as e:
        print(f"Error al obtener o mostrar habitaciones: {e}")

# Suponiendo que 'obtener_habitaciones' devuelve una lista de objetos con el atributo 'id'

def mostrar_examenes():
  print("-" * 40)
  print("Examenes")
  print("-" * 40)
  try:
    examenes = obtener_examenes()
    for examen in examenes:
      print(f"Rut:           {examen.rut_paciente or 'Sin registro'}")
      print(f"Examen:        {examen.nombre or 'Sin registro'}")
      print(f"Resultado:     {examen.resultado or 'Sin registro'}")
      print("-" * 40)
  except Exception as e:
    print(f"Error al obtener o mostrar examenes: {e}")

def mostrar_diagnosticos():
  print("-" * 40)
  print("Diagnosticos")
  print("-" * 40)
  try:
    diagnostico = obtener_diagnosticos()
    for diagnostico in diagnosticos:
      print(f"Rut:           {diagnostico.rut_paciente or 'Sin registro'}")
      print(f"Diagnostico:   {diagnostico.enfermedad or 'Sin registro'}")
      print("-" * 40)
  except Exception as e:
    print(f"Error al obtener o mostrar diagnostico: {e}")