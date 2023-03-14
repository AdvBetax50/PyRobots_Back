from fun.Partida import Partida
from fun.Sesion import SesionDB
from fun.ConexionWS  import ConexionWS

class  PartidaIniciar:

    def __init__(self, db_nombre):
        self.db_nombre = db_nombre
        self.db = SesionDB(db_nombre)

    def iniciarPartida(self,info_dic):
        if not self.db.existeNombreUsuario(info_dic["nombre_us"]):                                                               #comprobar que el usuario sea el creador 
            respuesta = "USUARIO_INVALIDO"
        elif not self.db.existePartida(info_dic["partida_id"]):
            respuesta = "PARTIDA_INVALIDA"
        elif self.db.estaTerminadaPartida(info_dic["partida_id"]):
            respuesta = "PARTIDA_TERMINADA"
        elif not self.db.esCreadorPartida(
                    info_dic["partida_id"], info_dic["nombre_us"]):
            respuesta = "USUARIO_NO_CREADOR"
        elif not self.db.esCantidadUsValida(info_dic["partida_id"]):
            respuesta = "FALTAN_JUGADORES"
        else:
            partida = Partida(self.db_nombre)
            partida.ejecutarPartida(info_dic)
            respuesta = {"exito":True}
            conexion = ConexionWS()
            conexion.actualizarResultadosWS(info_dic["partida_id"],True)
            self.db.terminarPartida(info_dic["partida_id"])
        return respuesta