from src.paciente import Paciente
from src.medico import Medico
from src.habitacion import Habitacion
from src.cama import Cama
from src.examen import Examen
from src.diagnostico import Diagnostico

from src.dummy_repositorio_clinica import agregar_paciente, agregar_medico, agregar_habitacion
# Agregar datos de prueba
def inicializar_datos():
    pacientes = [
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
    
    medicos = [
        ("Marcela", "González", "1010101-1"),
        ("Felipe", "Martínez", "2020202-2"),
        ("Carmen", "Rodríguez", "3030303-3"),
        ("Jorge", "López", "4040404-4"),
        ("Mónica", "García", "5050505-5")
    ]
    
    habitaciones = [ 'A', 'B', 'C', 'D', 'E' ]
    
    camas = [  1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
               11, 12, 13, 14, 15, 16, 17, 18,
               19, 20, 21, 22, 23, 24, 25, 26
    ]
    
    # Agregar pacientes
    for paciente in pacientes:
        agregar_paciente(Paciente(*paciente))
    
    # # Agregar médicos
    # for medico in medicos:
    #     agregar_medico(Medico(*medico))
    
    # # Agregar habitaciones
    # for habitacion in habitaciones:
    #     agregar_habitacion(Habitacion(habitacion))
    
    # # Agregar camas a habitaciones
    # for i in len(habitaciones):
    #     habitaciones[i].agregar_cama(Cama(camas[i]))
    
    # Asignar pacientes a camas



