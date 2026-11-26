import pyodbc

class SQLServer:

    def __init__(self):
        self.conexion = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DAVID;"
            "DATABASE=ClinicaSQL;"
            "Trusted_Connection=yes;"
        )

        self.cursor = self.conexion.cursor()

    def crear_cita(self,cita):
        """ Funcion que registra una cita en la base de datos"""

        self.cursor.execute("""
            INSERT INTO Citas(
                IdCliente,
                IdMedico,
                Fecha,
                HoraInicio,
                HoraFin,
                Estado
            )
            VALUES
            (?, ?, ?, ?, ?, ?)""", cita.id_cliente, cita.id_medico, cita.fecha, cita.hora_inicio, cita.hora_fin, cita.estado)
        self.conexion.commit()

    def buscar_cita_mismo_horario(self,id_medico,fecha,hora_inicio):
        """ Funcion para validar que no se registren citas a la misma hora"""

        self.cursor.execute(""" SELECT * FROM Citas WHERE IdMedico = ? AND Fecha = ? AND HoraInicio = ? AND Estado <> 'Cancelada'""", id_medico, fecha, hora_inicio)
        return self.cursor.fetchone()


    def listar_citas(self):
        """ Funcion que devuelve la lista de citas en la base de datos"""

        self.cursor.execute("""SELECT * FROM Citas""")
        return self.cursor.fetchall()


    def listar_citas_cliente(self,id_cliente):
        """ Funcion que devuelve el historial de citas de un cliente"""

        self.cursor.execute(
            """SELECT * FROM Citas WHERE IdCliente = ? ORDER BY Fecha DESC, HoraInicio DESC""",
            id_cliente
        )
        return self.cursor.fetchall()


    def listar_citas_medico_semana(self,id_medico,fecha_inicio,fecha_fin):
        """ Funcion que devuelve las citas de un medico dentro de un rango de fechas (semana)"""

        self.cursor.execute(
            """SELECT * FROM Citas WHERE IdMedico = ? AND Fecha BETWEEN ? AND ?
                AND Estado <> 'Cancelada' ORDER BY Fecha, HoraInicio""",
            id_medico, fecha_inicio, fecha_fin
        )
        return self.cursor.fetchall()


    def buscar_cita(self,id_cita):
        """ Funcion que busca una cita a la base de datos"""

        self.cursor.execute("""SELECT * FROM Citas WHERE IdCita = ?""", id_cita)
        return self.cursor.fetchone()


    def cancelar_cita(self,id_cita):
        """ Funcion que actualiza el estado de la cita a 'Cancelada' en la base de datos"""

        self.cursor.execute("""UPDATE Citas SET Estado = ? WHERE IdCita = ?""", "Cancelada", id_cita)
        self.conexion.commit()

    def modificar_cita(self,id_cita,fecha,hora_inicio,hora_fin):
        """ Funcion que modifica una cita"""

        self.cursor.execute("""UPDATE Citas SET Fecha = ?, HoraInicio = ?, HoraFin = ? WHERE IdCita = ?""", fecha, hora_inicio, hora_fin, id_cita)
        self.conexion.commit()


    def crear_factura(self,factura):
        """ Funcion que resgistra una factura a la base de datos"""

        self.cursor.execute("""INSERT INTO Facturas
            (
                IdCita,
                Servicio,
                Precio,
                IVA,
                Total,
                EstadoPago
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?
            )""",
        factura.id_cita,
        factura.servicio,
        factura.precio,
        factura.iva,
        factura.total,
        factura.estado_pago
        )
        self.conexion.commit()


    def listar_facturas(self):
        """ Funcion que retorna la lista de facturas registradas en la base de datos"""

        self.cursor.execute("""SELECT * FROM Facturas""")
        return self.cursor.fetchall()

    def buscar_factura(self,id_factura):
        """ Funcion para buscar facturas en la base de datos"""

        self.cursor.execute("""SELECT * FROM Facturas WHERE IdFactura = ?""", id_factura)
        return self.cursor.fetchone()

    def buscar_factura_cita(self,id_cita):
        """ Funcion para buscar una factura segun el ID de la cita"""
        self.cursor.execute("""SELECT * FROM Facturas WHERE IdCita = ?""", id_cita)
        return self.cursor.fetchone()