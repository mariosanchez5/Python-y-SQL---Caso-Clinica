from datetime import datetime

class Examen:
    def __init__(self, id, nombre, resultado, medico, paciente, fecha=datetime.now()):
        self.id = id
        self.nombre = nombre
        self.resultado = resultado
        self.rut_medico = medico
        self.rut_paciente = paciente
        self.fecha = fecha

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'resultado': self.resultado,
            'medico': rut_medico,
            'paciente': self.rut_paciente,
            'fecha': self.fecha
        }

    def to_row(self):
        return (self.id, self.nombre, self.resultado, self.rut_medico, self.rut_paciente, self.fecha)
