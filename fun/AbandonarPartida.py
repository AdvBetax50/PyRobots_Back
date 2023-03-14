import sys
sys.path.append("..")
from fun.Sesion import SesionDB
from fun.ConexionWS import ConexionWS

class AbandonarPartida:

    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
   
    def quitarUsuarioDePartida(self, datos):
        respuesta=""

        if not self.db.existeNombreUsuario(datos["nombre_us"]):
            respuesta = "USUARIO_INVALIDO"
        elif not self.db.existePartida(datos["partida_id"]):
            respuesta = "PARTIDA_INVALIDA"
        elif self.db.esCreadorPartida(datos["partida_id"], datos["nombre_us"]):
            respuesta = "USUARIO_CREADOR"
        elif not self.db.estaUnido(datos["partida_id"], datos["nombre_us"]):
            respuesta = "USUARIO_NO_UNIDO"
        else:
            exito = self.db.borrarUsuarioDePartida(datos)
            respuesta = {'exito': exito}   
            unidos = self.db.consultarCantidadUnidos(datos["partida_id"])
            conexion = ConexionWS()
            conexion.actualizarDatosWS(datos["partida_id"], unidos)
        return respuesta 
