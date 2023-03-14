import jwt

import sys
sys.path.append("..")
from fun.Sesion import SesionDB

class CheckLogIng:

    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
    
    def obtenerAvatarUsuario(self, nombre_usuario):
        return self.db.obtenerAvatarUsuarioDB(nombre_usuario)
        
    def loginShowUsuarios(self, infoUsuario):
        msg = { "result" : None, "token" : None }
        if not self.db.existeNombreUsuario(infoUsuario["nombre"]):
            msg = { "result" : "El usuario no existe en la base de datos",
                    "token" : None }
        elif not self.db.esValidoUsuario(infoUsuario["nombre"]):
            msg = { "result" : "El usuario no esta verificado",
                    "token" : None }
        else:
            if self.db.existeUsuarioContrasena(infoUsuario["nombre"], infoUsuario["contrasena"]):
                msg = { "result" : "El usuario existe y la contraseña es correcta",
                    "token" : jwt.encode({"usuario": infoUsuario["nombre"]}, "secret", algorithm="HS256")}
            else:
                msg = { "result" : "El usuario existe pero la contraseña es incorrecta",
                    "token" : None }
        return msg
            