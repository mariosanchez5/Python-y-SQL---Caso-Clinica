class diagnostico:
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

    def to_row(self):
        examenes = []
        for examen in self.examenes:
            examenes.append(examen.id)
        return (self.medico, self.enfermedad, self.paciente, examenes)