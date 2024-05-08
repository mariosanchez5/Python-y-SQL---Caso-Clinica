class Paciente:
    def __init__(self, n='', a='', r='', e='', g=''):
        self.__nombre = n
        self.__apellido = a
        self.__rut = r
        self.__edad = e
        self.__genero = g
    
    def GetNombre(self):
        return self.__nombre
    def GetApellido(self):
        return self.__apellido
    def GetRut(self):
        return self.__rut
    def GetEdad(self):
        return self.__edad
    def GetGenero(self):
        return self.__genero
    
    def SetNombre(self,n):
        self.__nombre = n
    def SetApellido(self,a):
        self.__apellido = a
    def SetRut(self,r):
        self.__rut = r
    def SetEdad(self,e):
        self.__edad = e
    def SetGenero(self,g):
        self.__genero = g

class Medico:
    def __init__(self, n='', a='', e=''):
        self.__nombre = n
        self.__apellido = a
        self.__especialidad = e
    
    def GetNombre(self):
        return self.__nombre
    def GetApellido(self):
        return self.__apellido
    def GetEspecialidad(self):
        return self.__especialidad
    
    def SetNombre(self,n):
        self.__nombre = n
    def SetApellido(self,a):
        self.__apellido = a
    def SetEspecialidad(self,e):
        self.__especialidad = e

class Examen:
    def __init__(self, n='', t=''):
        self.__nombrexamen = n
        self.__tipo = t
    
    def GetNombrexamen(self):
        return self.__nombrexamen
    def GetTipo(self):
        return self.__tipo
    
    def SetNombrexamen(self,n):
        self.__nombrexamen= n
    def SetTipo(self,t):
        self.__tipo = t

class Enfermedad:
    def __init__(self, n='', t=''):
        self.__nombrenfermedad = n
        self.__tipo = t
    
    def GetNombrenfermedad(self):
        return self.__nombrenfermedad
    def GetTipo(self):
        return self.__tipo
    
    def SetNombrenfermedad(self,n):
        self.__nombrenfermedad= n
    def SetTipo(self,t):
        self.__tipo = t

class Diagnostico:
    def __init__(self, d=''):
        self.__diagnostico = d
    
    def GetDiagnostico(self):
        return self.__diagnostico
    
    def SetDiagnostico(self,d):
        self.__diagnostico= d

class Habitacion:
    def __init__(self, n='', z=''):
        self.__ncamas = n
        self.__zona = z
    
    def GetNcamas(self):
        return self.__ncamas
    def GetZona(self):
        return self.__zona
    
    def SetNcamas(self,n):
        self.__ncamas= n
    def SetZona(self,z):
        self.__zona = z

class Cama:
    def __init__(self, d=''):
        self.__disponible = d
    
    def GetDisponible(self):
        return self.__disponible
    
    def SetDisponible(self,d):
        self.__disponible= d
