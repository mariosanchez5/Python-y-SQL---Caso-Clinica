class Paciente:
    def __init__(self, nombre, apellido, rut, medico_tratante=None, cama=None, diagnosticos=[], examenes=[], ultimo_examen=None):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.medico_tratante = medico_tratante
        self.cama = cama
        self.diagnosticos = diagnosticos.copy()
        self.examenes = examenes.copy()
        self.ultimo_examen = None
    
    def agregar_diagnostico(self, diagnostico):
        self.diagnosticos.append(diagnostico)

    def agregar_examen(self, examen):
        self.examenes.append(examen)
        self.ultimo_examen = examen

    def asignar_medico(self, medico):
        if self.medico_tratante:
            self.medico_tratante.quitar_paciente(self)
        self.medico_tratante = medico
        self.medico_tratante.agregar_paciente(self)

    def imprimir_paciente(self):
        print(f'Nombre: {self.nombre} - Apellido: {self.apellido} - Rut: {self.rut} - Médico tratante: {self.medico_tratante.nombre_completo()} - Cama: {self.cama}')
        if self.diagnosticos:
            print('Diagnósticos:')
            for diagnostico in self.diagnosticos:
                print(f'{diagnostico}')
        else:
            print('No hay diagnosticos')
        if self.examenes:
            print('Exámenes:')
            for examen in self.examenes:
                print(f'{examen}')
        else:
            print('No hay exámenes')
        if self.ultimo_examen:
            print(f'Último examen: {self.ultimo_examen}')

    def to_row(self):
        return (self.nombre, self.apellido, self.rut, self.medico_tratante, self.cama)
    
    def from_row(row):
        return Paciente(row[1], row[2], row[3], row[4], row[5])

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.rut == other.rut