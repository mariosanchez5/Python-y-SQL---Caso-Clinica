class Diagnostico:
    def __init__(self, medico, enfermedad, paciente, examenes):
        self.enfermedad = enfermedad
        self.examenes = examenes
        self.paciente = paciente
        self.medico = medico
    
    def imprimir_diagnostico(self):
        print(f'El médico: {self.medico.nombre_completo()} ha diagnosticado a {self.paciente.nombre} con {self.enfermedad}.')
        print(f'Se basó en los siguientes exámenes:')
        for examen in self.examenes:
            print(f'- {examen.nombre} - Resultado: {examen.resultado}')

    def to_dict(self):
        examenes = []
        for examen in self.examenes:
            examenes.append(examen.id)
        return {
            'medico': self.medico.rut,
            'enfermedad': self.enfermedad,
            'paciente': self.paciente.rut,
            'examenes': examenes
        }

    def to_row(self):
        examenes = []
        for examen in self.examenes:
            examenes.append(examen.id)
        return (self.medico, self.enfermedad, self.paciente, examenes)

    def __eq__(self, other):
        return self.medico == other.medico and self.enfermedad == other.enfermedad and self.paciente == other.paciente