class Habitacion:
    def __init__(self, id, camas=[]):
        self.camas = camas.copy() # Listado de objetos cama
        self.id = id
        self.disponible = False

    def agregar_cama(self, cama):
        self.camas.append(cama)

    def to_row(self):
        id_camas = []
        for cama in self.camas:
            id_camas.append(cama.id)
        return (self.id, id_camas)

    def imprimir():
        print(f'Habitación: {self.id}')
        for cama in self.camas:
            print(f'Cama: {cama.id} - Disponible: {cama.disponible}')

    def from_row(row):
        return None
