class Diagnostico:
    def __init__(self, medico, enfermedad, paciente, examenes):
        self.enfermedad = enfermedad
        self.id_examenes = examenes
        self.rut_paciente = paciente
        self.rut_medico = medico
    
    def to_dict(self):
        return {
            'medico': self.rut_medico,
            'enfermedad': self.enfermedad,
            'paciente': self.rut_paciente,
            'examenes': id_examenes
        }

    def to_row(self):
        return (self.medico, self.enfermedad, self.paciente, id_examenes)

    def __eq__(self, other):
        return self.medico == other.medico and self.enfermedad == other.enfermedad and self.paciente == other.paciente