import sys
sys.path.append("..")
from fun.Sesion import SesionDB
  
class RegistrarPartida:
    
    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)

    def esValidoJugadoresMin(self, jugadores_min):
        return 2 <= jugadores_min and jugadores_min <= 4

    def esValidoJugadoresMax(self, jugadores_max):
        return 2 <= jugadores_max and jugadores_max <= 4

    def esValidoJuegoTotales(self,juegos_totales):
        return 1 <= juegos_totales and juegos_totales <= 200
    
    def esValidoRondasTotales(self, rondas_totales):
        return 1 <= rondas_totales and rondas_totales <= 10000

    def registrarPartidaCreada(self, partida_dic):
        if (not self.esValidoJugadoresMin(partida_dic["jugadoresMin"])):
            respuesta = {"result":"JUGADORES_MIN_INVALIDO"}
        elif (not self.esValidoJugadoresMax(partida_dic["jugadoresMax"])):
            respuesta = {"result":"JUGADORES_MAX_INVALIDO"}
        elif (not self.esValidoJuegoTotales(partida_dic["juegosTotales"])):
            respuesta = {"result":"JUGOS_TOATALES_INVALIDO"}
        elif (not self.esValidoRondasTotales(partida_dic["rondasTotales"])):
            respuesta = {"result":"RONDAS_TOTALES_INVALIDO"}
        elif (not self.db.existeNombreUsuario(partida_dic["nombreUsuario"])):
            respuesta = {"result":"USUARIO_INVALIDO"}
        elif (not self.db.existeRobotUsuario(
                partida_dic["nombreUsuario"] ,
                partida_dic["robotUsuario"])):
            respuesta = {"result":"ROBOT_INVALIDO"}
        else:
            if (partida_dic["contrasena"] == None):
                partida_dic["contrasena"] = ""
            id = self.db.registrarPartidaCreadaDB(partida_dic)
            respuesta = {
                "websocket":"ws://localhost:5000/ws/unirse/"+str(id)}
        return respuesta
