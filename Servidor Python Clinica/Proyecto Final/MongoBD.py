from pymongo import MongoClient
from bson import ObjectId

class MongoBD:
    def __init__(self):
        self.cliente = MongoClient("mongodb://localhost:27017/") #SE CONECTA DIRECTAMENTE CON SQL
        self.db = self.cliente["ClinicaDB"] #SE A LA BASE DE DATOS DE CLINICA


        #---------------------#
        # FUNCIONES CRUD
        #---------------------#

        #USUARIOS
    def registrar_usuario(self, usuario):
        """ Funcion que registra un usuario en la base de datos """
        self.db.Usuarios.insert_one(usuario.ConvertirDiccionario())

    def listar_usuarios(self):

        """ Funcion que devuelve una lista con los usuarios de la base de datos """
        return list(self.db.Usuarios.find({}))

    def buscar_usuario(self, usuario):
        """ Funcion que busca un usuario por su nombre de usuario (login)"""
        return self.db.Usuarios.find_one({"usuario": usuario})

    def buscar_usuario_identificacion(self, identificacion):
        """ Funcion que busca el usuario ligado a una identificacion (cliente/empleado)"""
        return self.db.Usuarios.find_one({"identificacion": identificacion})

    def modificar_estado_usuario(self, identificacion, estado):
        """ Funcion que activa/desactiva el acceso (login) de un usuario segun su identificacion"""
        self.db.Usuarios.update_one(
            {"identificacion": identificacion},
            {"$set": {"estado": estado}}
        )


        #CLIENTES
        
    def registrar_cliente(self, cliente):
        """ Funcion que registra un cliente en la base de datos """
        self.db.Clientes.insert_one(cliente.ConvertirDiccionario())

    def listar_clientes(self):
        """ Funcion que devuelve una lista con los clientes de la base de datos """ 
        return list(self.db.Clientes.find({}))

    def buscar_cliente(self,identificacion):
        """ Funcion que busca un cliente en la base de datos"""
        return self.db.Clientes.find_one({"identificacion": identificacion})

    def eliminar_cliente(self,identificacion):
        """ Funcion que elimina un cliente de la base de datos"""
        self.db.Clientes.delete_one({"identificacion": identificacion})

    def modificar_cliente(self,identificacion,nuevos_datos):
        """ Funcion que actualiza los datos de un cliente"""
        self.db.Clientes.update_one(
            {"identificacion":identificacion},
            {"$set":nuevos_datos}
        )

    def cambiar_estado_cliente(self,identificacion,estado):
        """ Funcion que activa/desactiva a un cliente"""
        self.db.Clientes.update_one(
            {"identificacion": identificacion},
            {"$set": {"estado": estado}}
        )

        # MEDICOS

    def registrar_medico(self, medico):
        """ Funcion que registra un medico en la base de datos """
        self.db.Medicos.insert_one(medico.ConvertirDiccionario())

    def listar_medicos(self):
        """ Funcion que devuelve una lista con los medicos de la base de datos """
        return list(self.db.Medicos.find({}))

    def listar_medicos_por_especialidad(self, especialidad):
        """ Funcion que devuelve los medicos de una especialidad en concreto """
        return list(self.db.Medicos.find({"especialidad": especialidad}))

    def buscar_medico(self,identificacion):
        """ Funcion que busca un medico en la base de datos"""
        return self.db.Medicos.find_one({"identificacion": identificacion})

    def eliminar_medico(self,identificacion):
        """ Funcion que elimina a un medico de la base de datos"""
        self.db.Medicos.delete_one({"identificacion": identificacion}) 

    def modificar_medico(self, indentificacion, nuevos_datos):
        """ Funcion que actualzia los datos de un medico"""
        self.db.Medicos.update_one(
            {"identificacion":indentificacion},
            {"$set":nuevos_datos}
        )

        # ESPECIALIDADES
    
    def listar_especialidades(self):
        """ Funcion que devuelve una lista con las especialidades de la base de datos """
        return list(self.db.Especialidades.find({}))

    def registrar_especialidad(self,especialidad):
        """ Funcion que registra una especialidad"""
        self.db.Especialidades.insert_one(especialidad.ConvertirDiccionario())

    def buscar_especialidad(self,nombre):
        """ Funcion para buscar una especialidad en la base de datos"""
        return self.db.Especialidades.find_one({"nombre": nombre})

    def modificar_especialidad(self,nombre,nuevos_datos):
        """ Funcion que modifica una especialidad en la base de datos"""

        self.db.Especialidades.update_one(
            {"nombre": nombre},
            {"$set": nuevos_datos}
        )

    def eliminar_especialidad(self,nombre):
        """ Funcion que elimina una especialidad"""
        self.db.Especialidades.delete_one({"nombre": nombre})


        # HORARIOS
    
    def registrar_horario(self,horario):
        """ Funcion para registrar un horario en la base de datos"""
        self.db.Horarios.insert_one(horario.ConvertirDiccionario())

    def listar_horarios(self):
        """ Funcion que devuelve la lista de horarios registrados"""
        return list(self.db.Horarios.find({}))

    def buscar_horario(self,identificacionMedico):
        """ Funcion que busca los horarios de un medico (uno por dia de la semana)"""
        return list(self.db.Horarios.find({"identificacionMedico":identificacionMedico}))

    def modificar_horario(self,idHorario,nuevos_datos):
        """ Funcion para modificar un horario en la base de datos"""
        self.db.Horarios.update_one(
            {"_id":ObjectId(idHorario)},
            {"$set":nuevos_datos})

    def eliminar_horario(self,idHorario):
        """ Funcion para eliminar un horario de la base de datos"""
        self.db.Horarios.delete_one({"_id": ObjectId(idHorario)})

    def buscar_horario_id(self, idHorario):
        """ Funcion para buscar horario por id de mongo"""
        return self.db.Horarios.find_one({"_id": ObjectId(idHorario)})

    # EMPLEADOS
    def registrar_empleado(self, empleado):
        """ Funcion que registra un empleado"""
        self.db.Empleados.insert_one(empleado.ConvertirDiccionario())

    def listar_empleados(self):
        """ Funcion para listar los empleados registrados"""
        return list(self.db.Empleados.find({}))

    def buscar_empleado(self,identificacion):
        """ Funcion que busca un empleado en la base de datos"""
        return self.db.Empleados.find_one({"identificacion":identificacion})

    def modificar_empleado(self,identificacion,nuevos_datos):
        """ Funcion que modifica un empleado en la base de datos"""
        self.db.Empleados.update_one(
            {"identificacion":identificacion},
            {"$set":nuevos_datos}
        )

    def eliminar_empleado(self,identificacion):
        """ Funcion que elimina un empleado"""
        self.db.Empleados.delete_one({"identificacion":identificacion})

    def cambiar_estado_empleado(self,identificacion,estado):
        """ Funcion que activa/desactiva a un empleado"""
        self.db.Empleados.update_one(
            {"identificacion": identificacion},
            {"$set": {"estado": estado}}
        )

    def login(self, usuario, password):
        """ Funcion que valida el login de un usuario en la base de datos """
        resultado = self.db.Usuarios.find_one(
            {
                "usuario": usuario,
                "password": password,
                "estado": True
            }
        )
        return resultado
