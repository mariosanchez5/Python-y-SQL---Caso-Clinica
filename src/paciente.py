class Paciente:
    def __init__(self, nombre, apellido, rut, medico_tratante=None, cama=None, diagnosticos=[], examenes=[], ultimo_examen=None):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.rut_medico_tratante = medico_tratante
        self.id_cama = cama.id if cama else None
        self.id_habitacion = cama.id_habitacion if cama else None
        self.id_diagnosticos = diagnosticos.copy()
        self.id_examenes = examenes.copy()
        self.id_ultimo_examen = ultimo_examen

    def agregar_diagnostico(self, diagnostico):
        self.diagnosticos.append(diagnostico)

    def agregar_examen(self, examen):
        self.id_examenes.append(examen.id)
        self.id_ultimo_examen = examen.id

    def asignar_medico(self, medico):
        self.rut_medico_tratante = medico.rut

    def asignar_cama(self, cama):
        self.id_cama = cama.id
        self.id_habitacion = cama.id_habitacion

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rut': self.rut,
            'medico_tratante': self.rut_medico_tratante if self.rut_medico_tratante else None,
            'cama': self.id_cama if self.id_cama else None,
            'habitacion': self.id_habitacion if self.id_habitacion else None,
            'diagnosticos': self.id_diagnosticos,
            'examenes': self.id_examenes,
            'ultimo_examen': self.id_ultimo_examen if self.id_ultimo_examen else None
        }

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.rut == other.rut