class Horario:

    def __init__(self, identificacionMedico, diaSemana, horaInicio, horaFin, ):
        self.identificacionMedico = identificacionMedico
        self.diaSemana = diaSemana
        self.horaInicio = horaInicio
        self.horaFin = horaFin

    def ConvertirDiccionario(self):
        """ Funcion que convierte de objeto horario a diccionario"""

        return {
            "identificacionMedico":self.identificacionMedico,
            "diaSemana":self.diaSemana,
            "horaInicio":self.horaInicio,
            "horaFin":self.horaFin,
        }
