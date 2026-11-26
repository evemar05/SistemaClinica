class Factura:

    def __init__(self,id_cita,servicio,precio,iva,total,estado_pago):
        self.id_cita = id_cita
        self.servicio = servicio
        self.precio = precio
        self.iva = iva
        self.total = total
        self.estado_pago = estado_pago