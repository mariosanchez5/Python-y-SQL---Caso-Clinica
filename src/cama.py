class Cama:
    def __init__(self, id, disponible=True, habitacion=None):
        self.disponible = disponible
        self.habitacion = habitacion
        self.id = id

    def ocupar(self):
        self.disponible = False
    
    def desocupar(self):
        self.disponible = True

    def to_row(self):
        return (self.id, self.disponible, self.habitacion)
    
    def from_row(row):
        return cama(row[1], row[2], row[3])

    # Redefinir el operador de igualdad
    def __eq__(self, other):
        return self.id == other.id