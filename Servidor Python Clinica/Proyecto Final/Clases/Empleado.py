class Empleado:
    def __init__(self,identificacion,nombre,telefono,email,puesto,estado=True):
        self.identificacion = identificacion
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.puesto = puesto
        self.estado = estado

    def ConvertirDiccionario(self):
        """ Funcion que convierte de objeto empleado a diccionario"""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "puesto": self.puesto,
            "estado": self.estado
        }