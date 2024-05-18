class Medico:
    def __init__(self, nombre, apellido, rut, pacientes=[]):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.pacientes = pacientes.copy()

    def agregar_paciente(self, paciente):
        for p in self.pacientes:
            if p.rut == paciente.rut:
                return
        self.pacientes.append(paciente)
    
    def quitar_paciente(self, paciente):
        for p in self.pacientes:
            if p.rut == paciente.rut:
                self.pacientes.remove(p)

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rut': self.rut,
            'rut_pacientes': [paciente.rut for paciente in self.pacientes]
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