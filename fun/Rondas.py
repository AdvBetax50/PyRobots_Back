import numpy as np
import math
import timeout_decorator

from fun.RobotEnJuego import *
from fun.MisilDeRobot import *
from fun.Constante import *

class Rondas:

    def calculoDistanciaImpacto(self,x1,y1,x2,y2):
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)

    def calculoNuevasPosiociones(self, listaMisil):
        for misil in listaMisil:
            if misil.dist <= VELOCIDAD_MISIL:
                posicion_misil_x = misil.posicion_misil[0] + round(
                    misil.dist * math.cos(math.radians(misil.orientacion)))
                posicion_misil_y = misil.posicion_misil[1] + round(
                    misil.dist * math.sin(math.radians(misil.orientacion)))
                misil.dist = 0
            else:
                posicion_misil_x = misil.posicion_misil[0] + round(
                    VELOCIDAD_MISIL * math.cos(math.radians(misil.orientacion)))
                posicion_misil_y = misil.posicion_misil[1] + round(
                    VELOCIDAD_MISIL * math.sin(math.radians(misil.orientacion)))
                if (999 <= posicion_misil_x or posicion_misil_x <= 0 or 
                    999 <= posicion_misil_y or posicion_misil_y <= 0) :
                    misil.dist = 0
                else:
                    misil.dist -= VELOCIDAD_MISIL
            if 999 <= posicion_misil_x:
                posicion_misil_x = 999
            if 0 >= posicion_misil_x:
                posicion_misil_x = 0   
            if 999 <= posicion_misil_y:
                posicion_misil_y = 999
            if 0 >= posicion_misil_y:
                posicion_misil_y = 0
            misil.posicion_misil = (posicion_misil_x,posicion_misil_y)
    
    def dispararNuevosMisiles(self,listaRobot):
        listaMisiles = []
        for robot in listaRobot:
            #Cannon tiene que estar listo y el robot con vida
            if(robot.robot.canionEstado and robot.robotVivo() and robot.robot.is_cannon_ready()):
                robot.robot.disparrowHecho()
                posActual_x = robot.robot.posicion[0]
                posActual_y = robot.robot.posicion[1]
                ang = robot.robot.canonDireccion["angulo"]
                dist = robot.robot.canonDireccion["distancia"]
                listaMisiles.append(MisilDeRobot(posActual_x,posActual_y, ang, dist))
                robot.robot.canionEstado = False
            else:
                robot.robot.rondaSinDisparrow()
        return listaMisiles

    def listaDeMisilesExplotados(self,listaMisiles):
        coordenadasExplosiones = []
        for misil in listaMisiles:
            if misil.dist == 0:
                coordenadasExplosiones.append(misil.posicion_misil)
                misil.explosionMisil()
        return coordenadasExplosiones

    def coalisionConMisiles(self, listaRobot, listaCoordenadasMisiles):
        for robot in listaRobot:
            for explosion in listaCoordenadasMisiles:
                distanciaImpacto = self.calculoDistanciaImpacto(
                    robot.robot.posicion[0], robot.robot.posicion[1], 
                    explosion[0], explosion[1])
                if distanciaImpacto < 5:
                    robot.robot.vida -= DAÑO_POR_EXPLOCION_5M
                elif distanciaImpacto < 20:
                    robot.robot.vida -= DAÑO_POR_EXPLOCION_20M
                elif distanciaImpacto < 40:
                    robot.robot.vida -= DAÑO_POR_EXPLOCION_40M
                if (robot.robot.vida < 0):
                    robot.robot.vida = 0

    def calcularRonda(self,ronda_actual):
        #Scannear, dispara y moverse
        for robot_en_ronda in ronda_actual["robots"]:
           if(robot_en_ronda.robot.escaneadora["resolucion"] != 0 and
                        robot_en_ronda.robotVivo()):
                robot_en_ronda.escanear(ronda_actual["robots"])

        #Actualizamos la posición de los misiles
        self.calculoNuevasPosiociones(ronda_actual["misiles"])

        #Disparamos los nuevos misiles
        ronda_actual["misiles"] += self.dispararNuevosMisiles(ronda_actual["robots"])

        # Buscamos las coordenadas de impacto
        coordenadasExplosiones = self.listaDeMisilesExplotados(ronda_actual["misiles"])
        self.coalisionConMisiles(ronda_actual["robots"],coordenadasExplosiones)

        for robot_en_ronda in ronda_actual["robots"]:
            if(robot_en_ronda.robotVivo()):
                robot_en_ronda.moverRobot()
        
        RobotEnJuego.infligirDañoPorChoqueEntreRobots(ronda_actual["robots"])

        for robot_en_ronda in ronda_actual["robots"]:
            if(robot_en_ronda.robot.vida > 1 ):
                robot_en_ronda.rondas_vivos += 1


    def iniciarRonda(self, configuracion):
        lista_robots = []
        numero_robot = len(configuracion["robots"])
        for id in configuracion["robots"]:
            robot_nuevo = RobotEnJuego(id)
            robot_nuevo.setPosicionRobot()
            try:
                robot_nuevo.loc[robot_nuevo.nombre_clase].initialize(robot_nuevo.robot)
            except:
                robot_nuevo.robot.vida = 0
            robot_nuevo.posicion_fin_del_juego = numero_robot + 1
            lista_robots.append(robot_nuevo)   
        return lista_robots
    
    @timeout_decorator.timeout(1)
    def ejecucionResponds(self, robot):
        robot.loc[robot.nombre_clase].responds(robot.robot)

    def avanzarRonda(self, estado_ronda):
        for robot in estado_ronda["robots"]:
            if(robot.robot.vida > 0):
                try:
                    self.ejecucionResponds(robot)
                except:
                    robot.robot.vida = 0
        self.calcularRonda(estado_ronda)
        robots_ronda = []
        misiles_ronda = []

        for rob in estado_ronda["robots"]:              
            robot = dict(
                id = rob.id_robot,
                nombre = rob.nombre,
                pos_x = rob.robot.posicion[0],
                pos_y = rob.robot.posicion[1],
                estado = rob.robot.vida,
                vision = 0,
                canon = 0,
                velocidad=rob.robot.get_velocity())
            robots_ronda.append(robot)
        for misil in estado_ronda["misiles"]:
            misiles = dict(                     
                pos_x = misil.posicion_misil[0],
                pos_y = misil.posicion_misil[1],
                orientacion = misil.orientacion,
                explotado = misil.explotado,
                distancia = misil.dist)
            misiles_ronda.append(misiles)

        lista_misil_copia = []
        for misil in estado_ronda["misiles"]:
            if not misil.explotado:
                lista_misil_copia.append(misil)
        estado_ronda["misiles"]=lista_misil_copia.copy()
        return {"robots" : robots_ronda, "misiles" : misiles_ronda}