import math
import random
import numpy as np

from fun.Sesion import SesionDB
from fun.Constante import *

class RobotEnJuego:

    def __init__(self,id):
        self.id_robot = id
        self.nombre = ""
        self.avatar = ""
        self.loc = {}
        self.tamañoDelRobot = TAMAÑO_ROBOT 
        self.posicion_fin_del_juego = 0
        self.rondas_vivos = 0
        self.glo = {"Robot": Robot}
        self.db = SesionDB('example.sqlite')
        self.codigo = self.db.stringRobot(id)
        try:
            exec(self.codigo, self.glo, self.loc)
            self.nombre_clase = list(self.loc.keys())[0]
            self.robot = self.loc[self.nombre_clase]()
        except:
            self.robot = Robot()
            self.robot.vida = 0
            
    def robotVivo(self):
        return self.robot.vida > 0

    def setPosicionRobot(self):
        self.robot.posicion = (random.randint(0,999), random.randint(0,999))

    def escanear(self, lista_robot):                                    
        angulo_dir = self.robot.escaneadora["direccion"]
        resolucion = self.robot.escaneadora["resolucion"]
        angulo_max = angulo_dir + resolucion
        angulo_min = angulo_dir - resolucion
        distancia_escaneada = MAX_DISTANCIA
        if angulo_max > 360:
            max_superior = angulo_max - 360
            max_inferior = 0
            min_superior = 360
            min_inferior = angulo_min
        elif angulo_min < 0:
            max_superior = angulo_max
            max_inferior = 0
            min_superior = 360
            min_inferior = 360 + angulo_min
        else:
            max_superior = angulo_max
            max_inferior = angulo_dir
            min_superior = angulo_dir
            min_inferior = angulo_min
        for robot in lista_robot:
            if(not robot.robotVivo()):
                continue
            robot_angulo = robot.calcularAngulo( self.robot.posicion,
                    robot.robot.posicion)
            if ((min_inferior <= robot_angulo and robot_angulo <= min_superior) or
                    (max_inferior <= robot_angulo and robot_angulo <= max_superior)):
                distancia_robot = robot.calcularDistancia(
                        self.robot.posicion, robot.robot.posicion)
                if (distancia_robot < distancia_escaneada and distancia_robot != 0 ):
                    distancia_escaneada = distancia_robot
        if(distancia_escaneada != MAX_DISTANCIA):
            self.robot.distanciaScaneo = distancia_escaneada
        else:
            self.robot.distanciaScaneo = 0
        self.robot.escaneadora["direccion"] = 0
        self.robot.escaneadora["resolucion"] = 0

    def calcularDistancia(self, punto1, punto2):
        x1 = punto1[0] 
        x2 = punto1[1]
        y1 = punto2[0]
        y2 = punto2[1]
        return np.sqrt((y1-x1)**2 + (y2-x2)**2)

    def calcularAngulo(self, punto1, punto2):
        px1 = punto1[0] 
        py1 = punto1[1]
        px2 = punto2[0]
        py2 = punto2[1]
        x = px2-px1
        y = py2-py1
        angulo = math.atan2(y, x) * (180.0 / math.pi)
        if angulo < 0:
            angulo = 360 + angulo
        return angulo

    def moverRobot(self):
        nuevaPosicionX = self.robot.posicion[0] + round(
                ((self.robot.movimiento["velocidad"] / 100) * 
                VELOCIDAD_MAXIMA_ROBOT * math.cos(
                math.radians(self.robot.movimiento["direccion"]))))
        nuevaPosicionY = self.robot.posicion[1] + round(
                ((self.robot.movimiento["velocidad"] / 100) * 
                VELOCIDAD_MAXIMA_ROBOT * math.sin(
                math.radians(self.robot.movimiento["direccion"]))))
        if(nuevaPosicionX < 0 or nuevaPosicionX > 999 or 
            nuevaPosicionY < 0 or nuevaPosicionY > 999 ): 
            if nuevaPosicionX  > 999:
                nuevaPosicionX = 999
            if nuevaPosicionY > 999:  
                nuevaPosicionY = 999
            if nuevaPosicionX  < 0: 
                nuevaPosicionX = 0
            if nuevaPosicionY  < 0:
                nuevaPosicionY  = 0
            self.robot.vida -= DAÑO_POR_CHOQUE
        self.robot.posicion=(nuevaPosicionX, nuevaPosicionY)

    def infligirDañoPorChoqueEntreRobots(lista_robots):
        for i in range( len(lista_robots) ):
            if(not lista_robots[i].robotVivo()):
                continue
            posRobI = lista_robots[i].robot.posicion
            p1 = (posRobI[0],posRobI[1])
            for j in range(i+1,len(lista_robots)):
                if(not lista_robots[j].robotVivo()):
                    continue
                posRobJ = lista_robots[j].robot.posicion
                p2 = (posRobJ[0],posRobJ[1])
                if math.dist(p1 ,p2) <= TAMAÑO_ROBOT:
                    lista_robots[i].restarVidaPorChoqque()
                    lista_robots[j].restarVidaPorChoqque()

    def restarVidaPorChoqque(self):
        if self.robot.vida - DAÑO_POR_CHOQUE < 0:
            self.robot.vida = 0
        else:
            self.robot.vida -= DAÑO_POR_CHOQUE

class Robot:
    def __init__(self) :
        self.canonDireccion = { "angulo" : 0 , "distancia" : 0}
        self.canionEstado = False
        self.escaneadora = {"direccion" : 0, "resolucion" : 0}
        self.distanciaScaneo = 0
        self.movimiento = {"direccion": 0, "velocidad" : 0}
        self.rondasSinDisparar = 0
        self.vida = 100
        self.posicion = (0,0)

    def rondaSinDisparrow(self):
        self.rondasSinDisparar -= 1

    def disparrowHecho(self):
        self.rondasSinDisparar = RONDAS_SIN_DISPARAR

    def point_scanner(self, direction, resolution_in_degree):
        if(resolution_in_degree < 0 or
            resolution_in_degree > 20):
            resolution_in_degree = 0
        self.escaneadora["direccion"] = direction
        self.escaneadora["resolucion"] = resolution_in_degree
         
    def scanned(self):
        return self.distanciaScaneo

    def cannon(self, degree, distancia):
        self.canonDireccion["angulo"] = degree
        self.canonDireccion["distancia"] = distancia
        self.canionEstado = True
        
    def drive(self, direction, velocity):
        if(velocity > 49 or direction< 0 or direction>360):
            direction = self.movimiento["direccion"]
        self.movimiento = {"direccion": direction, "velocidad" : velocity}

    def is_cannon_ready(self):
        return self.rondasSinDisparar == 0

    # METODOS GET
    def get_direction(self):
        return self.movimiento["direccion"]
    
    def get_velocity(self):
        return self.movimiento["velocidad"]
    
    def get_position(self):
        return self.posicion
    
    def get_damage(self):
        return self.vida