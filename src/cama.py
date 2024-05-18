class Cama:
    def __init__(self, id, disponible=True, habitacion=None):
        self.disponible = disponible
        self.id_habitacion = habitacion
        self.rut_paciente = None
        self.id = id

    def ocupar(self, paciente):
        self.rut_paciente = paciente.rut
        self.disponible = False
    
    def desocupar(self):
        self.disponible = True
        self.rut_paciente = None

    def asignar_habitacion(self, habitacion):
        self.id_habitacion = habitacion.id

    def to_row(self):
        return (self.id, self.disponible, self.id_habitacion)
    
    def from_row(row):
        return cama(row[1], row[2], row[3])

    def to_dict(self):
        resultado = {
            'id': self.id,
            'disponible': self.disponible,
            'habitacion': self.id_habitacion,
        }
        if self.rut_paciente:
            resultado['paciente'] = self.rut_paciente
        return resultado

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.id == other.id