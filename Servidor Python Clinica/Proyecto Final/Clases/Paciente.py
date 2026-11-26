class Paciente:
    def __init__(self,identificacion,nacionalidad,nombre,primer_apellido,segundo_apellido,telefono,email,padecimientos,estado=True):
        self.identificacion = identificacion
        self.nacionalidad = nacionalidad
        self.nombre = nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.telefono = telefono
        self.email = email
        self.padecimientos = padecimientos
        self.estado = estado

    def ConvertirDiccionario(self):
        """ Funcion que convierte de objeto Paciente a diccionario"""
        return {
            "identificacion": self.identificacion,
            "nacionalidad": self.nacionalidad,
            "nombre": self.nombre,
            "primerApellido": self.primer_apellido,
            "segundoApellido": self.segundo_apellido,
            "telefono": self.telefono,
            "email": self.email,
            "padecimientos": self.padecimientos,
            "estado": self.estado
        }


    def __str__(self):
        return f"{self.identificacion} - {self.nombre}"
