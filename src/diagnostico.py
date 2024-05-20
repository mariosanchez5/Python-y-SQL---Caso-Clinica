class Diagnostico:
    def __init__(self, id, medico, enfermedad, paciente, examenes):
        self.id = id
        self.enfermedad = enfermedad
        self.id_examenes = examenes
        self.rut_paciente = paciente
        self.rut_medico = medico
    
    def to_dict(self):
        return {
            'id': self.id,
            'medico': self.rut_medico,
            'enfermedad': self.enfermedad,
            'paciente': self.rut_paciente,
            'examenes': self.id_examenes
        }

    def __eq__(self, other):
        return self.rut_medico == other.rut_medico and self.rut_paciente == other.rut_paciente