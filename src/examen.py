from datetime import datetime

class Examen:
    def __init__(self, id, nombre, resultado, medico, paciente, fecha=datetime.now()):
        self.id = id
        self.nombre = nombre
        self.resultado = resultado
        self.medico = medico
        self.paciente = paciente
        self.fecha = fecha

    def imprimir_examen(self):
        print(f'Reporte de examen {self.id}')
        print(f'Fecha: {self.fecha}')
        print(f'Paciente: {self.paciente.nombre} {self.paciente.apellido}')
        print(f'Médico: {self.medico.nombre} {self.medico.apellido}')
        print(f'Nombre: {self.nombre}')
        print(f'Resultado: {self.resultado}')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'resultado': self.resultado,
            'medico': self.medico.rut,
            'paciente': self.paciente.rut,
            'fecha': self.fecha
        }

    def to_row(self):
        return (self.id, self.nombre, self.resultado, self.medico, self.paciente, self.fecha)
