class Cita:
    
    def __init__(self,id_cliente,id_medico,fecha,hora_inicio,hora_fin,estado="Pendiente"):
        self.id_cliente = id_cliente
        self.id_medico = id_medico
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado