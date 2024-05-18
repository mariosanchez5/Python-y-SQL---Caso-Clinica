class Medico:
    def __init__(self, nombre, apellido, rut, pacientes=[]):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.pacientes = pacientes.copy()
    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)
    
    def quitar_paciente(self, paciente):
        self.pacientes.remove(paciente)

    def imprimir_medico(self):
        print(f'Nombre: {self.nombre} - Apellido: {self.apellido} - Rut: {self.rut}')
        if self.pacientes:
            print('Pacientes:')
            for paciente in self.pacientes:
                print(f'{paciente.nombre} {paciente.apellido}')
        else:
            print('No tiene pacientes')

    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    def to_row(self):
        return (self.nombre, self.apellido, self.rut)

    def from_row(row):
        return Medico(row[1], row[2], row[3])

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.rut == other.rut