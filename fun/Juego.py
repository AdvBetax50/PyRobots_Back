from fun.Rondas import Rondas
from fun.Constante import *

class Juego:

    def __init__(self):
        self.robot_id_ganador = 0
        self.empate = False
        
    def iniciarJuego(self, configuracion):
        rondas = Rondas()
        lista_robots = rondas.iniciarRonda(configuracion)
        numero_de_robots = len(configuracion["robots"])
        dic_informacion_simulacion = {"simulacion":[], "resultado":[]}
        ronda_actual = {"robots":lista_robots, "misiles":[]}
        
        for _ in range(0, configuracion["rondas"]):
            nueva_ronda = rondas.avanzarRonda(ronda_actual)                 
            dic_informacion_simulacion["simulacion"].append(nueva_ronda)
            if (self.terminoJuego(lista_robots)):
                break
        
        dic_informacion_simulacion["resultado"] = self.getResultados(lista_robots,numero_de_robots)
        return dic_informacion_simulacion

    def calcularResultado(self, lista_robots, numero_de_robots):
        posicion = 1
        count_robot = 0
        max_rondas = 0
        ignorar = MAX_INT

        lista_robots_copia = lista_robots.copy()
        while(posicion != numero_de_robots + 1):
            for robot in lista_robots_copia:
                if(robot.rondas_vivos > max_rondas and
                robot.rondas_vivos < ignorar):
                    max_rondas = robot.rondas_vivos

            for robot in lista_robots_copia:
                if(robot.rondas_vivos == max_rondas):
                    robot.posicion_fin_del_juego = posicion
                    count_robot += 1
            posicion += count_robot
            count_robot = 0
            ignorar = max_rondas
            max_rondas = 0
            
    def getResultados(self, lista_robots, numero_de_robots):                 
        resultado_robots = []
        self.calcularResultado(lista_robots, numero_de_robots)
        for robot in lista_robots:
            robot_resultado = dict(
                id = robot.id_robot,
                posicion = robot.posicion_fin_del_juego)
            resultado_robots.append(robot_resultado)
        return resultado_robots

    def terminoJuego(self, lista_robot):
        robot_vivos = 0
        for rob in lista_robot:  
            if 0 < rob.robot.vida :
                robot_vivos += 1
        return robot_vivos < 2