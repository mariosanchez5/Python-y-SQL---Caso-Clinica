class Habitacion:
    def __init__(self, id, camas=[]):
        self.id_camas = camas.copy()
        self.id = id

    def agregar_cama(self, cama):
        self.id_camas.append(cama.id)

    def quitar_cama(self, cama):
        self.id_camas.remove(cama.id)

    def to_row(self):
        return (self.id, id_camas)

    def from_row(row):
        return Habitacion(row[1], row[2])

    def to_dict(self):
        return {
            'id': self.id,
            'camas': self.id_camas
        }
