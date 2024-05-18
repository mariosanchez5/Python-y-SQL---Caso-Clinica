class Paciente:
    def __init__(self, nombre, apellido, rut, medico_tratante=None, cama=None, diagnosticos=[], examenes=[], ultimo_examen=None):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.medico_tratante = medico_tratante
        self.cama = cama
        self.habitacion = cama.habitacion if cama else None
        self.diagnosticos = diagnosticos.copy()
        self.examenes = examenes.copy()
        self.ultimo_examen = None
    
    def agregar_diagnostico(self, diagnostico):
        self.diagnosticos.append(diagnostico)

    def agregar_examen(self, examen):
        self.examenes.append(examen)
        self.ultimo_examen = examen

    def asignar_medico(self, medico):
        self.medico_tratante = medico

    def asignar_cama(self, cama):
        self.cama = cama
        self.habitacion = cama.habitacion

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rut': self.rut,
            'medico_tratante': self.medico_tratante.rut if self.medico_tratante else None,
            'cama': self.cama.id if self.cama else None,
            'habitacion': self.habitacion.id if self.habitacion else None,
            'diagnosticos': [diagnostico.to_dict() for diagnostico in self.diagnosticos],
            'examenes': [examen.to_dict() for examen in self.examenes],
            'ultimo_examen': self.ultimo_examen.to_dict() if self.ultimo_examen else None
        }

    def to_row(self):
        return (self.nombre, self.apellido, self.rut, self.medico_tratante, self.cama)
    
    def from_row(row):
        # (id, nombre, apellido, rut, medico_tratante, cama)
        return Paciente(
            nombre=row[1], 
            apellido=row[2], 
            rut=row[3], 
            medico_tratante=row[4], 
            cama=row[5]
        )

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.rut == other.rut