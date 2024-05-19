class Medico:
    def __init__(self, nombre, apellido, rut, pacientes=[]):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.rut_pacientes = pacientes.copy()

    def agregar_paciente(self, paciente):
        for p in self.rut_pacientes:
            if p == paciente.rut:
                return
        self.rut_pacientes.append(paciente.rut)
    
    def quitar_paciente(self, paciente):
        for p in self.rut_pacientes:
            if p == paciente.rut:
                self.rut_pacientes.remove(p)

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rut': self.rut,
            'rut_pacientes': self.rut_pacientes
        }

    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    def to_row(self):
        return (self.nombre, self.apellido, self.rut)

    def from_row(row):
        return Medico(row[1], row[2], row[3])

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.rut == other.rut