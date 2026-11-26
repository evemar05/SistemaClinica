class Especialidad:
    def __init__(self,nombre,descripcion):
        self.nombre = nombre
        self.descripcion = descripcion


    def ConvertirDiccionario(self):
        """ Funcion que convierte de objeto Especialidad a diccionario"""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }