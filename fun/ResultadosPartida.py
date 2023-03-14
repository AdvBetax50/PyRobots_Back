import sys
sys.path.append("..")
from fun.Sesion import SesionDB

class ResultadosPartida:
    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
    
    def obtenerResultados(self, datos):
        respuesta = ""
        if (not self.db.existeNombreUsuario(datos["nombre_us"]) 
                or not self.db.estaUnido(datos["partida_id"], datos["nombre_us"])):
            respuesta = "USUARIO_INVALIDO"
        elif (not self.db.existePartida(datos["partida_id"]) 
                or not self.db.estaTerminadaPartida(datos["partida_id"])):
            respuesta = "PARTIDA_INVALIDA"
        else:
            respuesta = self.db.obtenerResultadosPartida(datos["partida_id"]) 
        return respuesta
