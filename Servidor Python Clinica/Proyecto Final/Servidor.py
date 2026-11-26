#IMPORTES PARA EL SERVER
import socket
import threading
import json


#IMPORTACION DE TODAS LAS CLASES
from Clases.Paciente import Paciente
from Clases.Medico import Medico
from Clases.Usuario import Usuario
from Clases.Cita import Cita
from Clases.Horario import Horario
from Clases.Empleado import Empleado
from Clases.Facturas import Factura
from Clases.Especialidad import Especialidad
from MongoBD import MongoBD
from SQLBD import SQLServer


from datetime import datetime, timedelta  #PARA LAS CITAS

IVA = 0.13  #PORCENTAJE DE IVA UTILIZADO PARA FACTURAR SERVICIOS
DIAS_ANTICIPACION_CITA = 2  #DIAS MINIMOS DE ANTICIPACION PARA MODIFICAR/CANCELAR UNA CITA


# FUNCION DE LOGIN
def login(datos):
    """ Funcion que valida el login de un usuario en la base de datos """
    usuario = datos["usuario"]
    password = datos["password"]
    resultado = mongo.login(usuario, password)

    if resultado:
        return {
            "estatus": 0,
            "mensaje": "Login correcto",
            "datos": {
                "usuario": resultado["usuario"],
                "rol": resultado["rol"],
                "identificacion": resultado.get("identificacion", "")
            }
            }
    return {
        "estatus": -1,
        "mensaje":
        "Credenciales incorrectas"
    }


# FUNCIONES DE LISTADO
def listarClientes():
    """ Funcion que devuelve una lista con los clientes de la base de datos """
    lista = mongo.listar_clientes()
    clientes = []

    for cliente in lista:
        cliente["_id"] = str(cliente["_id"])

        clientes.append(cliente)

    return {
        "estatus": 0,
        "mensaje": "Lista de clientes obtenida correctamente",
        "datos": clientes
    }

def buscar_cliente(datos):
    """ Funcion que busca un cliente registrado"""

    cliente = mongo.buscar_cliente(datos["identificacion"])
    if cliente:
        cliente["_id"] = str(cliente["_id"])
        return {
            "estatus": 0,
            "mensaje":
            "Cliente encontrado",
            "datos":cliente
        }

    return {
        "estatus": -1,
        "mensaje":
        "Cliente no encontrado"
    }

def modificar_cliente(datos):
    """ Funcion que modifica un cliente"""
    identificacion = datos["identificacion"]
    nuevos_datos = {
            "nacionalidad":datos["nacionalidad"],
            "nombre":datos["nombre"],
            "primerApellido":datos["primerApellido"],
            "segundoApellido":datos["segundoApellido"],
            "telefono":datos["telefono"],
            "email":datos["email"]
        }
    
    mongo.modificar_cliente(identificacion,nuevos_datos)

    return {
        "estatus": 0,
        "mensaje":
            "Cliente modificado"
    }

def eliminar_cliente(datos):
    """ Funcion que elimina un cliente"""

    mongo.eliminar_cliente(datos["identificacion"])
    return {
        "estatus": 0,
        "mensaje": "Cliente eliminado"
    }

def cambiar_estado_cliente(datos):
    """ Funcion que activa o desactiva a un cliente (y su acceso al sistema)"""

    cliente = mongo.buscar_cliente(datos["identificacion"])
    if not cliente:
        return {
            "estatus": -1,
            "mensaje": "El cliente no existe"
        }

    mongo.cambiar_estado_cliente(datos["identificacion"], datos["estado"])
    mongo.modificar_estado_usuario(datos["identificacion"], datos["estado"])

    return {
        "estatus": 0,
        "mensaje": "Estado del cliente actualizado"
    }

def listar_especialidades():
    """ Funcion para listar las especialidades"""

    lista = mongo.listar_especialidades()
    especialidades = []

    for especialidad in lista:
        especialidad["_id"] = str(especialidad["_id"])
        especialidades.append(especialidad)

    return {
        "estatus": 0,
        "mensaje":
        "Especialidades obtenidas",
        "datos": especialidades
    }

def listarMedicos():
    """ Funcion que devuelve una lista con los medicos de la base de datos """
    lista = mongo.listar_medicos()
    medicos = []

    for medico in lista:
        medico["_id"] = str(medico["_id"])

        medicos.append(medico)

    return {
        "estatus": 0,
        "mensaje": "Lista de medicos obtenida correctamente",
        "datos": medicos

    }


def listar_medicos_especialidad(datos):
    """ Funcion que devuelve los medicos que pertenecen a una especialidad"""

    lista = mongo.listar_medicos_por_especialidad(datos["especialidad"])
    medicos = []
    for medico in lista:
        medico["_id"] = str(medico["_id"])
        medicos.append(medico)

    return {
        "estatus": 0,
        "mensaje": "Medicos obtenidos",
        "datos": medicos
    }


def buscar_medico(datos):
    """ Funcion que busca un medico"""

    medico = mongo.buscar_medico(datos["identificacion"])
    if medico:
        medico["_id"] = str(medico["_id"])
        return {
            "estatus": 0,

            "mensaje": "Medico encontrado",
            "datos": medico
        }
    return {
        "estatus": -1,
        "mensaje": "Medico no encontrado"
    }


def buscar_especialidad(datos):
    """ Funcion para buscar una especilidad"""

    especialidad = mongo.buscar_especialidad(datos["nombre"])
    if especialidad:
        especialidad["_id"] = str(especialidad["_id"])

        return {
            "estatus": 0,
            "datos": especialidad
        }

    return {
        "estatus": -1,
        "mensaje": "Especialidad no encontrada"
    }


def modificar_especialidad(datos):
    """ Funcion para modificar una especlidad"""

    mongo.modificar_especialidad(datos["nombre"],{"descripcion": datos["descripcion"]})
    return {
        "estatus": 0,
        "mensaje": "Especialidad modificada"
    }


def modificar_medico(datos):
    """ Funcion que modifica un medico"""

    identificacion = datos["identificacion"]
    nuevos_datos = {
        "nombre":datos["nombre"],
        "telefono":datos["telefono"],
        "email":datos["email"],
        "especialidad":datos["especialidad"]
        }
    
    mongo.modificar_medico(identificacion,nuevos_datos)
    return {
        "estatus": 0,
        "mensaje": "Medico modificado"
    }

def eliminar_medico(datos):
    """ Funcion para eliminar un medico"""

    mongo.eliminar_medico(datos["identificacion"])
    return {
        "estatus": 0,
        "mensaje": "Medico eliminado"
    }


def listar_citas():
    """ Funcion que devuelve la lsita de citas registradas en SQL"""

    lista = SQL.listar_citas()
    citas = []
    for cita in lista:
        citas.append({
            "idCita": cita.IdCita,
            "idCliente": cita.IdCliente,
            "idMedico": cita.IdMedico,
            "fecha": str(cita.Fecha),
            "horaInicio": str(cita.HoraInicio),
            "horaFin": str(cita.HoraFin),
            "estado": cita.Estado
        })

    return {
        "estatus": 0,
        "mensaje":
        "Citas obtenidas",
        "datos": citas
    }

def buscar_cita(datos):
    """ Funcion que busca una cita en la base de datos"""

    cita = SQL.buscar_cita(datos["idCita"])
    if cita:
        return {
            "estatus": 0,
            "mensaje": "Cita encontrada",
            "datos": {
                "idCita": cita.IdCita,
                "idCliente": cita.IdCliente,
                "idMedico": cita.IdMedico,
                "fecha": str(cita.Fecha),
                "horaInicio": str(cita.HoraInicio),
                "horaFin": str(cita.HoraFin),
                "estado": cita.Estado
            }
        }

    return {
        "estatus": -1,
        "mensaje": "Cita no encontrada"
    }


def modificar_cita(datos):
    """ Funcion que modifica una cita en la base de datos.
    Solo se permite si faltan al menos DIAS_ANTICIPACION_CITA para la cita actual"""

    cita = SQL.buscar_cita(datos["idCita"])
    if not cita:
        return {
            "estatus": -1,
            "mensaje": "La cita no existe"
        }

    if not tiene_anticipacion(cita.Fecha):
        return {
            "estatus": -1,
            "mensaje": f"La cita solo puede modificarse con al menos {DIAS_ANTICIPACION_CITA} dias de anticipacion"
        }

    SQL.modificar_cita(
        datos["idCita"],
        datos["fecha"],
        datos["horaInicio"],
        datos["horaFin"]
    )

    return {
        "estatus": 0,
        "mensaje": "Cita modificada"
    }

def cancelar_cita(datos):
    """ Funcion que modifica el estado de la cita a 'Cancelada'.
    Solo se permite si faltan al menos DIAS_ANTICIPACION_CITA para la cita actual"""

    cita = SQL.buscar_cita(datos["idCita"])
    if not cita:
        return {
            "estatus": -1,
            "mensaje": "La cita no existe"
        }

    if not tiene_anticipacion(cita.Fecha):
        return {
            "estatus": -1,
            "mensaje": f"La cita solo puede cancelarse con al menos {DIAS_ANTICIPACION_CITA} dias de anticipacion"
        }

    SQL.cancelar_cita(datos["idCita"])
    return {
        "estatus": 0,
        "mensaje": "Cita cancelada"
    }


def tiene_anticipacion(fecha_cita):
    """ Funcion auxiliar que valida si una fecha de cita cumple con los dias
    minimos de anticipacion respecto de hoy """

    if isinstance(fecha_cita, str):
        fecha_cita = datetime.strptime(fecha_cita, "%Y-%m-%d")
    else:
        fecha_cita = datetime(fecha_cita.year, fecha_cita.month, fecha_cita.day)

    hoy = datetime.now()
    hoy = datetime(hoy.year, hoy.month, hoy.day)

    return (fecha_cita - hoy).days >= DIAS_ANTICIPACION_CITA


def listar_citas_cliente(datos):
    """ Funcion que devuelve el historial de citas de un cliente"""

    lista = SQL.listar_citas_cliente(datos["idCliente"])
    citas = []
    for cita in lista:
        citas.append({
            "idCita": cita.IdCita,
            "idCliente": cita.IdCliente,
            "idMedico": cita.IdMedico,
            "fecha": str(cita.Fecha),
            "horaInicio": str(cita.HoraInicio),
            "horaFin": str(cita.HoraFin),
            "estado": cita.Estado
        })

    return {
        "estatus": 0,
        "mensaje": "Historial de citas obtenido",
        "datos": citas
    }


def obtener_rango_semana(fecha_str):
    """ Funcion auxiliar que devuelve el lunes y domingo de la semana de una fecha dada"""

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    inicio = fecha - timedelta(days=fecha.weekday())
    fin = inicio + timedelta(days=6)
    return inicio, fin


def listar_citas_medico_semana(datos):
    """ Funcion que devuelve las citas (asignadas) de un medico en la semana de la
    fecha indicada, incluyendo los datos basicos del cliente de cada cita """

    medico = mongo.buscar_medico(datos["idMedico"])
    if not medico:
        return {
            "estatus": -1,
            "mensaje": "El medico no existe"
        }

    inicio, fin = obtener_rango_semana(datos["fecha"])

    lista = SQL.listar_citas_medico_semana(
        datos["idMedico"],
        inicio.strftime("%Y-%m-%d"),
        fin.strftime("%Y-%m-%d")
    )

    citas = []
    for cita in lista:
        cliente = mongo.buscar_cliente(cita.IdCliente)
        citas.append({
            "idCita": cita.IdCita,
            "fecha": str(cita.Fecha),
            "horaInicio": str(cita.HoraInicio),
            "horaFin": str(cita.HoraFin),
            "estado": cita.Estado,
            "identificacionCliente": cliente["identificacion"] if cliente else cita.IdCliente,
            "nombreCliente": cliente["nombre"] if cliente else "",
            "telefonoCliente": cliente["telefono"] if cliente else "",
            "emailCliente": cliente["email"] if cliente else ""
        })

    return {
        "estatus": 0,
        "mensaje": "Horario de la semana obtenido",
        "datos": {
            "inicioSemana": inicio.strftime("%Y-%m-%d"),
            "finSemana": fin.strftime("%Y-%m-%d"),
            "citas": citas
        }
    }


def disponibilidad_semana(datos):
    """ Funcion que devuelve el horario de un medico para la semana de la fecha
    indicada junto con las citas ya ocupadas, para calcular la disponibilidad """

    medico = mongo.buscar_medico(datos["idMedico"])
    if not medico:
        return {
            "estatus": -1,
            "mensaje": "El medico no existe"
        }

    horarios = mongo.buscar_horario(datos["idMedico"])
    inicio, fin = obtener_rango_semana(datos["fecha"])

    citas_ocupadas = SQL.listar_citas_medico_semana(
        datos["idMedico"],
        inicio.strftime("%Y-%m-%d"),
        fin.strftime("%Y-%m-%d")
    )

    ocupadas = [
        {"fecha": str(cita.Fecha), "horaInicio": str(cita.HoraInicio)}
        for cita in citas_ocupadas
    ]

    return {
        "estatus": 0,
        "mensaje": "Disponibilidad obtenida",
        "datos": {
            "inicioSemana": inicio.strftime("%Y-%m-%d"),
            "finSemana": fin.strftime("%Y-%m-%d"),
            "horario": horarios,
            "ocupadas": ocupadas
        }
    }


def eliminar_especialidad(datos):
    """ Funcion para eliminar una especialidad"""

    mongo.eliminar_especialidad(datos["nombre"])
    return {
        "estatus": 0,
        "mensaje": "Especialidad eliminada"
    }


def listar_facturas():
    """ Funcion que devuelve la lista de las facturas registradas"""

    lista = SQL.listar_facturas()
    facturas = []
    for factura in lista:
        facturas.append({
            "idFactura": factura.IdFactura,
            "idCita": factura.IdCita,
            "servicio": factura.Servicio,
            "precio": float(factura.Precio),
            "total": float(factura.Total)
        })

    return {
        "estatus": 0,
        "mensaje": "Facturas obtenidas",
        "datos": facturas
    }

def listar_horarios():
    """Funcion para listar horarios"""

    lista = mongo.listar_horarios()
    horarios = []
    for horario in lista:
        horario["_id"] = str(horario["_id"])
        horarios.append(horario)

    return {
        "estatus": 0,
        "mensaje": "Horarios obtenidos",
        "datos": horarios
    }

def listar_empleados():
    """Funcion para listar empleados"""

    lista = mongo.listar_empleados()
    empleados = []
    for empleado in lista:
        empleado["_id"] = str(empleado["_id"])
        empleados.append(empleado)

    return {
        "estatus": 0,
        "mensaje": "Empleados obtenidos",
        "datos": empleados
    }

def buscar_empleado(datos):
    """Funcion para buscar empleado"""

    empleado = mongo.buscar_empleado(datos["identificacion"])
    if empleado:
        empleado["_id"] = str(empleado["_id"])

        return {
            "estatus": 0,
            "mensaje": "Empleado encontrado",
            "datos": empleado
        }
    
    return {
        "estatus": -1,
        "mensaje": "Empleado no encontrado"
    }


def modificar_empleado(datos):
    """Funcion para modificar empleado"""

    nuevos_datos = {
        "telefono":datos["telefono"],
        "email":datos["email"],
        "puesto":datos["puesto"]
    }
    mongo.modificar_empleado(datos["identificacion"],nuevos_datos)

    return {
        "estatus": 0,
        "mensaje": "Empleado modificado"
    }


def eliminar_empleado(datos):
    """Funcion para eliminar empleado"""

    mongo.eliminar_empleado(datos["identificacion"])
    return {
        "estatus": 0,
        "mensaje": "Empleado eliminado"
    }

def cambiar_estado_empleado(datos):
    """Funcion que activa o desactiva a un empleado (y su acceso al sistema).
    Un empleado inactivo no puede ingresar al aplicativo"""

    empleado = mongo.buscar_empleado(datos["identificacion"])
    if not empleado:
        return {
            "estatus": -1,
            "mensaje": "El empleado no existe"
        }

    mongo.cambiar_estado_empleado(datos["identificacion"], datos["estado"])
    mongo.modificar_estado_usuario(datos["identificacion"], datos["estado"])

    return {
        "estatus": 0,
        "mensaje": "Estado del empleado actualizado"
    }


def buscar_horario(datos):
    """Funcion para buscar horarios de un medico"""

    horarios = mongo.buscar_horario(datos["identificacionMedico"])
    if horarios:
        for horario in horarios:
            horario["_id"] = str(horario["_id"])

        return {
            "estatus": 0,
            "mensaje": "Horarios encontrados",
            "datos": horarios
        }

    return {
        "estatus": -1,
        "mensaje": "No existen horarios"
    }

def modificar_horario(datos):
    """Funcion para modificar horario"""

    nuevos_datos = {
        "diaSemana":datos["diaSemana"],
        "horaInicio":datos["horaInicio"],
        "horaFin":datos["horaFin"]
    }

    mongo.modificar_horario(datos["identificacionMedico"],nuevos_datos)
    return {
        "estatus": 0,
        "mensaje": "Horario modificado"
    }


def eliminar_horario(datos):
    """Funcion para eliminar horario"""

    mongo.eliminar_horario(datos["identificacionMedico"])

    return {
        "estatus": 0,
        "mensaje": "Horario eliminado"
    }

def buscar_horario_id(datos):
    """ Funcion para buscar horario por ID"""

    horario = mongo.buscar_horario_id(datos["idHorario"])
    if horario:
        horario["_id"] = str(horario["_id"])

        return {
            "estatus": 0,
            "mensaje": "Horario encontrado",
            "datos": horario
        }

    return {
        "estatus": -1,
        "mensaje": "Horario no encontrado"
    }


# FUNCIONES DE REGISTRO
def registrar_cliente(datos):
    """ Funcion para registrar un cliente. Registra tanto sus datos personales
    como su usuario de acceso (login) al sistema """

    cliente = mongo.buscar_cliente(datos["identificacion"])
    medico = mongo.buscar_medico(datos["identificacion"])
    empleado = mongo.buscar_empleado(datos["identificacion"])
    if cliente or medico or empleado:
        return {
            "estatus": -1,
            "mensaje": "La identificacion ya se encuentra registrada en el sistema"
        }

    usuario_existente = mongo.buscar_usuario(datos["usuario"])
    if usuario_existente:
        return {
            "estatus": -1,
            "mensaje": "El nombre de usuario ya se encuentra en uso"
        }

    paciente = Paciente(
        datos["identificacion"],
        datos["nacionalidad"],
        datos["nombre"],
        datos["primerApellido"],
        datos["segundoApellido"],
        datos["telefono"],
        datos["email"],
        datos["padecimientos"]
    )
    mongo.registrar_cliente(paciente)

    usuario = Usuario(datos["usuario"], datos["password"], "cliente")
    usuario_dict = usuario.ConvertirDiccionario()
    usuario_dict["identificacion"] = datos["identificacion"]
    mongo.db.Usuarios.insert_one(usuario_dict)

    return {
        "estatus": 0,
        "mensaje": "Cliente Registrado"
    }

def registrar_medico(datos):
    """ Funcion para registrar un medico"""

    cliente = mongo.buscar_cliente(datos["identificacion"]) # VALIDACION DE IDENTIFICACION 
    medico = mongo.buscar_medico(datos["identificacion"])
    empleado = mongo.buscar_empleado(datos["identificacion"])

    if cliente or medico or empleado:

        return {
            "estatus": -1,
            "mensaje":
            "La identificacion ya se encuentra registrada en el sistema"
        }
    
    
    medico = Medico(
        datos["identificacion"],
        datos["nombre"],
        datos["telefono"],
        datos["email"],
        datos["especialidad"]
    )
    mongo.registrar_medico(medico)
    return {
        "estatus": 0,
        "mensaje": "Medico registrado"
    }

def registrar_especialidad(datos):
    """ Funcion para registrar una especialidad"""

    existente = mongo.buscar_especialidad(datos["nombre"])
    if existente:
        return {
            "estatus": -1,
            "mensaje": "La especialidad ya existe"
        }

    especialidad = Especialidad(
        datos["nombre"],
        datos["descripcion"]
    )

    mongo.registrar_especialidad(especialidad)
    return {
        "estatus": 0,
        "mensaje": "Especialidad registrada"
    }


def registrar_horario(datos):
    """Funcion para registrar un horario"""

    medico = mongo.buscar_medico(datos["identificacionMedico"])
    if not medico:
        return {
        "estatus": -1,
        "mensaje": "El medico no existe"
        }

    horarios = mongo.buscar_horario(datos["identificacionMedico"])
    for horario in horarios:
        if horario["diaSemana"] == datos["diaSemana"]:
            return {
                "estatus": -1,
                "mensaje": "Ya existe un horario para ese día"
            }
        
    horario = Horario(
        datos["identificacionMedico"],
        datos["diaSemana"],
        datos["horaInicio"],
        datos["horaFin"]
    )

    mongo.registrar_horario(horario)
    return {
        "estatus": 0,
        "mensaje": "Horario registrado"
    }

def registrar_empleado(datos):
    """Funcion para registrar un empleado. Solo puede registrarlo otro empleado activo"""

    cliente = mongo.buscar_cliente(datos["identificacion"])
    medico = mongo.buscar_medico(datos["identificacion"])
    existente = mongo.buscar_empleado(datos["identificacion"])
    if existente or cliente or medico:
        return {
            "estatus": -1,
            "mensaje": "La identificacion ya se encuentra registrada en el sistema"
        }

    usuario_existente = mongo.buscar_usuario(datos["usuario"])
    if usuario_existente:
        return {
            "estatus": -1,
            "mensaje": "El nombre de usuario ya se encuentra en uso"
        }

    empleado = Empleado(
        datos["identificacion"],
        datos["nombre"],
        datos["telefono"],
        datos["email"],
        datos["puesto"]
    )

    mongo.registrar_empleado(empleado)

    usuario = Usuario(datos["usuario"], datos["password"], "empleado")
    usuario_dict = usuario.ConvertirDiccionario()
    usuario_dict["identificacion"] = datos["identificacion"]
    mongo.db.Usuarios.insert_one(usuario_dict)

    return {
        "estatus": 0,
        "mensaje": "Empleado registrado"
    }


def crear_cita(datos):
    """ Funcion para registrar una cita"""

    fecha_cita = datetime.strptime(datos["fecha"],"%Y-%m-%d")   #FECHA DE LA CITA
    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"] #LISTA CON LOS DIAS DE LA SEMANA
    dia_cita = dias[fecha_cita.weekday()]
    horario_valido = False


    
    #VALIDAR QUE EXISTA UN CLIENTE
    cliente = mongo.buscar_cliente(datos["idCliente"])
    if not cliente:
        return {
            "estatus": -1,
            "mensaje": "El cliente no existe"
        }

    #VALIDAR QUE EXISTA UN MEDICO
    medico = mongo.buscar_medico(datos["idMedico"])
    if not medico:
        return {
            "estatus": -1,
            "mensaje": "El medico no existe"
        }    
    #VALIDAR QUE EXISTEN HORARIOS REGISTRADOS POR ESE MEDICO
    horarios = mongo.buscar_horario(datos["idMedico"])
    if not horarios:
        return {
            "estatus": -1,
            "mensaje": "El medico no tiene horarios registrados"
        }

    #VALIDAR QUE EL MEDICO TRABAJA ESE DIA
    for horario in horarios:
        if horario["diaSemana"] == dia_cita:
            horario_valido = True
            break
    if not horario_valido:
        return {
            "estatus": -1,
            "mensaje": "El medico no trabaja ese dia"
        }

    #VALIDAR QUE LA CITA REGISTRADA SE ENCUENTRE DENTRO DEL HORARIO DEL MEDICO
    hora_cita = datos["horaInicio"]
    horarioValido = False

    for horario in horarios:
        if horario["diaSemana"] == dia_cita:
            if (horario["horaInicio"] <= hora_cita < horario["horaFin"]):
                horarioValido = True
                break
    if not horarioValido:
        return {
            "estatus": -1,
            "mensaje": "La hora se encuentra fuera del horario del medico"
        }

    #VALIDAR QUE NO EXISTA CITA REGISTRADA EN LA HORA INGRESADA
    cita_existente = SQL.buscar_cita_mismo_horario(
        datos["idMedico"],
        datos["fecha"],
        datos["horaInicio"]
    )
    if cita_existente:
        return {
            "estatus": -1,
            "mensaje": "Ya existe una cita en ese horario"
        }
    
    cita = Cita(
        datos["idCliente"],
        datos["idMedico"],
        datos["fecha"],
        datos["horaInicio"],
        datos["horaFin"]
    )

    SQL.crear_cita(cita)
    return {
        "estatus": 0,
        "mensaje": "Cita creada correctamente"
    }


def crear_factura(datos):
    """ Funcion que registra una factura"""

    #VALIDAR QUE EXISTA UNA CITA
    cita = SQL.buscar_cita(datos["idCita"])
    if not cita:
        return {
            "estatus": -1,
            "mensaje": "La cita no existe"
        }
    #VALIDAR QUE LA CITA NO SE ENCUENTRE 'CANCELADA'
    if cita.Estado == "Cancelada":
        return {
            "estatus": -1,
            "mensaje": "No se puede facturar una cita cancelada"
        }
    #VALIDAR QUE NO EXISTA UNA FACTURA PARA ESA CITA
    factura_existente = SQL.buscar_factura_cita(datos["idCita"])
    if factura_existente:
        return {
            "estatus": -1,
            "mensaje": "La cita ya fue facturada"
        }

    #EL SERVIDOR CALCULA EL IVA Y EL TOTAL A PARTIR DEL PRECIO DEL SERVICIO
    precio = float(datos["precio"])
    monto_iva = round(precio * IVA, 2)
    total = round(precio + monto_iva, 2)

    factura = Factura(
        datos["idCita"],
        datos["servicio"],
        precio,
        monto_iva,
        total,
        "Pagado"
    )
    SQL.crear_factura(factura)

    return {
        "estatus": 0,
        "mensaje": "Factura creada",
        "datos": {
            "servicio": datos["servicio"],
            "precio": precio,
            "iva": monto_iva,
            "total": total
        }
    }


def buscar_factura_cita(datos):
    """ Funcion que busca la factura asociada a una cita"""

    factura = SQL.buscar_factura_cita(datos["idCita"])
    if factura:
        return {
            "estatus": 0,
            "mensaje": "Factura encontrada",
            "datos": {
                "idFactura": factura.IdFactura,
                "idCita": factura.IdCita,
                "servicio": factura.Servicio,
                "precio": float(factura.Precio),
                "iva": float(factura.IVA),
                "total": float(factura.Total),
                "estadoPago": factura.EstadoPago
            }
        }

    return {
        "estatus": -1,
        "mensaje": "No existe factura para esa cita"
    }

def ping():
    """ Funcion para comprobar la conexion de MVC con el Servidor Python"""
    return {
        "estatus": 0,
        "mensaje": "Servidor funcionando"
    }

#FUNCIONES DE SERVIDOR
def procesarAccion(datos):
    """ Funcion que procesa la accion recibida al servidor """
    accion = datos["accion"]

    if accion == "login":
        return login(datos)
    
    elif accion == "registrar_cliente":
        return registrar_cliente(datos)
    
    elif accion == "listarClientes":
        return listarClientes()

    elif accion == "buscar_cliente":
        return buscar_cliente(datos)

    elif accion == "modificar_cliente":
        return modificar_cliente(datos)

    elif accion == "eliminar_cliente":
        return eliminar_cliente(datos)

    elif accion == "cambiar_estado_cliente":
        return cambiar_estado_cliente(datos)

    elif accion == "registrar_medico":
        return registrar_medico(datos)
    
    elif accion == "listar_medicos":
        return listarMedicos()

    elif accion == "listar_medicos_especialidad":
        return listar_medicos_especialidad(datos)
    
    elif accion == "buscar_medico":
        return buscar_medico(datos)

    elif accion == "modificar_medico":
        return modificar_medico(datos)
    
    elif accion == "eliminar_medico":
        return eliminar_medico(datos)

    elif accion == "registrar_especialidad":
        return registrar_especialidad(datos)

    elif accion == "listar_especialidades":
        return listar_especialidades()

    elif accion == "buscar_especialidad":
        return buscar_especialidad(datos)

    elif accion == "modificar_especialidad":
        return modificar_especialidad(datos)

    elif accion == "eliminar_especialidad":
        return eliminar_especialidad(datos)

    elif accion == "registrar_empleado":
        return registrar_empleado(datos)

    elif accion == "listar_empleados":
        return listar_empleados()

    elif accion == "buscar_empleado":
        return buscar_empleado(datos)

    elif accion == "modificar_empleado":
        return modificar_empleado(datos)

    elif accion == "eliminar_empleado":
        return eliminar_empleado(datos)

    elif accion == "cambiar_estado_empleado":
        return cambiar_estado_empleado(datos)
    
    elif accion == "registrar_horario":
        return registrar_horario(datos)

    elif accion == "listar_horarios":
        return listar_horarios()

    elif accion == "buscar_horario":
        return buscar_horario(datos)

    elif accion == "modificar_horario":
        return modificar_horario(datos)

    elif accion == "buscar_horario_id":
        return buscar_horario_id(datos)

    elif accion == "eliminar_horario":
        return eliminar_horario(datos)
    
    elif accion == "crear_factura":
        return crear_factura(datos)

    elif accion == "listar_facturas":
        return listar_facturas()

    elif accion == "buscar_factura_cita":
        return buscar_factura_cita(datos)
    
    elif accion == "crear_cita":
        return crear_cita(datos)

    elif accion == "listar_citas":
        return listar_citas()

    elif accion == "listar_citas_cliente":
        return listar_citas_cliente(datos)

    elif accion == "listar_citas_medico_semana":
        return listar_citas_medico_semana(datos)

    elif accion == "disponibilidad_semana":
        return disponibilidad_semana(datos)

    elif accion == "buscar_cita":
        return buscar_cita(datos)

    elif accion == "modificar_cita":
        return modificar_cita(datos)

    elif accion == "cancelar_cita":
        return cancelar_cita(datos)
    
    elif accion == "ping":
        return ping()
    
    else:
        return {
            "estatus": -1,
            "mensaje": "Accion no válida"
        }


def procesar_cliente(cliente):
    """ Funcion que procesa la conexion de un cliente al servidor """
    try:
        recibido = cliente.recv(4096)

        texto = recibido.decode("utf-8")

        print("\nMensaje recibido")
        print(texto)

        datos = json.loads(texto)
        respuesta = procesarAccion(datos)
        cliente.send(json.dumps(respuesta).encode("utf-8"))

    except Exception as error:
        error = {
            "estatus": -1,
            "mensaje": str(error)
        }
        cliente.send(json.dumps(error).encode("utf-8"))

    finally:
        cliente.close()

print("INICIANDO SERVIDOR...")
mongo = MongoBD()
SQL = SQLServer()

host = "localhost"
port = 8000

servidor = socket.socket()

servidor.bind((host, port))

servidor.listen(5)

print("Servidor iniciado")

while True:
    cliente, direccion = servidor.accept()
    print(f"Cliente: {direccion}")
    hilo = threading.Thread(target=procesar_cliente,args=(cliente,))
    hilo.start()