

import sys
sys.path.append("..")
from fun.Sesion import SesionDB
from fun.ConexionWS import ConexionWS

class UnirsePartida:

    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
        
    def unirNuevoUsuario(self, datos):
        respuesta = ""
        if (datos["contrasena"] == None):
            datos["contrasena"] = ''
        
        if not self.db.existeNombreUsuario(datos["nombre_us"]):
            respuesta = "USUARIO_INVALIDO"
        elif not self.db.existePartida(datos["partida_id"]):
            respuesta = "PARTIDA_INVALIDA"
        elif self.db.estaLlenaPartida(datos["partida_id"]):
            respuesta = "PARTIDA_LLENA"
        elif self.db.estaUnido(datos["partida_id"], datos["nombre_us"]):
            respuesta = "USUARIO_YA_UNIDO"
        elif not self.db.existeRobotUsuario(datos["nombre_us"], datos["robot_id"]):
            respuesta = "ROBOT_INVALIDO"
        elif (self.db.tieneContrasena(datos["partida_id"]) and 
                not self.db.esCorrectaContrasena(datos["partida_id"], datos["contrasena"])):
            respuesta = "CONTRASENA_INVALIDA"
        else:
            self.db.registrarUsuarioEnPartida(datos)
            respuesta = {
                "websocket":"ws://localhost:5000/ws/unirse/"+str(datos["partida_id"])}
            unidos = self.db.consultarCantidadUnidos(datos["partida_id"])
            conexion = ConexionWS()
            conexion.actualizarDatosWS(datos["partida_id"], unidos)
        return respuesta