class Usuario:
    def __init__(self,usuario,password,rol,estado=True):
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.estado = estado

    def ConvertirDiccionario(self):
        """ Funcion que convierte un objeto Usuario a diccionario, para poner manipalarlo con Mongo"""
        return {
            "usuario": self.usuario,
            "password": self.password,
            "rol": self.rol,
            "estado": self.estado
        }

    def registrar_usuario(self,usuario):
        """ Registra en la base de datos"""
        self.db.Usuarios.insert_one(usuario.ConvertirDiccionario())

    def login(self,usuario,password):
        """ Valida el login con la base de datos"""
        return self.db.Usuarios.find_one(
            {
                "usuario": usuario,
                "password": password,
                "estado": True
            }
        )

    def __str__(self):
        return f"{self.usuario} - {self.rol}"