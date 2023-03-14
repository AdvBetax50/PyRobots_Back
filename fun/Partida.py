from fun.Juego import Juego
from fun.Sesion import SesionDB

class Partida:
    
    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)

    def ejecutarPartida(self, dic_id):
        lista_resultados=[]
        partida_confi= self.db.obtenerDatosPartidas(dic_id["partida_id"])
        juego_partida_confi = dict(
            rondas = partida_confi["rondas"],
            robots = partida_confi["robots"])
        for juego in range(0,partida_confi["juegos"]):
            juego = Juego()
            resultado = juego.iniciarJuego(juego_partida_confi)
            lista_resultados.append(resultado["resultado"])
        lista_resultado_dic = self.cargarResulatadosDic(lista_resultados,dic_id["partida_id"])
        self.calcularResultadoPartida(lista_resultado_dic)
        self.db.registrarResultados(lista_resultado_dic)
        return lista_resultado_dic
        
    def cargarResulatadosDic(self, lista_resultados, id_partida):    
        resultado_dic = []
        lista_resultado_robot = lista_resultados[0]
        for resultado_juego in lista_resultado_robot:
            robot_resultado_dic = dict(
                robot = resultado_juego["id"],
                partida = id_partida,
                robot_resultado = "",
                juegos_ganados = 0 , 
                juegos_perdidos = 0 ,
                juegos_empatados = 0)
            resultado_dic.append(robot_resultado_dic)
        for lista_resultado in lista_resultados:
            for pos_en_lista in range(0,len(lista_resultado)):
                if(not self.empateJuego(lista_resultado)):
                    if(lista_resultado[pos_en_lista]["posicion"] == 1 ):
                        resultado_dic[pos_en_lista]["juegos_ganados"] += 1
                    else:
                        resultado_dic[pos_en_lista]["juegos_perdidos"] += 1
                else:
                    if(lista_resultado[pos_en_lista]["posicion"] == 1 ):
                        resultado_dic[pos_en_lista]["juegos_empatados"] += 1
                    else:
                        resultado_dic[pos_en_lista]["juegos_perdidos"] += 1
        return resultado_dic

    def calcularResultadoPartida(self, lista_resultado_dic):
        max_partidas_ganadas = 0
        empate = self.empatePartida(lista_resultado_dic)
        for robot in lista_resultado_dic:
            if robot["juegos_ganados"] > max_partidas_ganadas:
                max_partidas_ganadas = robot["juegos_ganados"]
        for robot in lista_resultado_dic:
            if (empate and robot["juegos_ganados"] == max_partidas_ganadas and
                    robot["juegos_empatados"] > robot["juegos_perdidos"]):
                robot["robot_resultado"] = "Empate"
            elif ( not empate and robot["juegos_ganados"] == max_partidas_ganadas):
                robot["robot_resultado"] = "Ganador"
            else:
                robot["robot_resultado"] = "Perdedor"
        return lista_resultado_dic

    def empateJuego(self, resultado_juego):
        robot_posicion_1 = 0
        for robot in resultado_juego:
            if(robot["posicion"] == 1 ):
                robot_posicion_1 += 1
        return robot_posicion_1 != 1

    def empatePartida(self,lista_resultado_dic):
        robot_posicion_1 = 0
        max_partidas_ganadas = 0
        for robot in lista_resultado_dic:
            if robot["juegos_ganados"] > max_partidas_ganadas:
                max_partidas_ganadas = robot["juegos_ganados"]
        for robot in lista_resultado_dic:
            if(robot["juegos_ganados"] == max_partidas_ganadas):
                robot_posicion_1 += 1
        return robot_posicion_1 != 1