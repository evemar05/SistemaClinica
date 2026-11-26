class Medico:
    def __init__(self,identificacion,nombre,telefono,email,especialidad,estado=True):
        self.identificacion = identificacion
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.especialidad = especialidad
        self.estado = estado


    def ConvertirDiccionario(self):
        """ Funcion que convierte de objeto Medico a diccionario"""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "especialidad": self.especialidad,
            "estado": self.estado
        }


