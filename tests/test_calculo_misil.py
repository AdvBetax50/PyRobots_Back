from unittest import TestCase, mock
import math

from fun.Rondas import Rondas
from fun.RobotEnJuego import RobotEnJuego
from fun.MisilDeRobot import MisilDeRobot

class TestMockValue(TestCase):
    
    def test_calculo_de_distancia(self):
        simulacionRonda = Rondas()
        punto1 = (0,4)
        punto2 = (3,0)
        distancia = simulacionRonda.calculoDistanciaImpacto(punto1[0],punto1[1], punto2[0], punto2[1])
        assert(distancia == 5)

    def test_calculo_nueva_posicion_con_dist(self):
        clasePrueba = Rondas()
        misil_1 = MisilDeRobot(0,0,30,350)
        misil_2 = MisilDeRobot(0,0,30,450)
        clasePrueba.calculoNuevasPosiociones([misil_1, misil_2])
        # 0,866025404
        assert(misil_1.posicion_misil[0] == (round(math.cos(math.radians(30))*100) + 0))
        assert(misil_1.posicion_misil[1] == (round(math.sin(math.radians(30))*100) + 0))
        assert(misil_1.dist == (350-100))
        assert(misil_2.posicion_misil[0] == (round(math.cos(math.radians(30))*100) + 0))
        assert(misil_2.posicion_misil[1] == (round(math.sin(math.radians(30))*100) + 0))
        assert(misil_2.dist == (450-100))

    def test_calculo_nueva_posicion_yendose_del_tablero_con_dist(self):
        clasePrueba = Rondas()
        misil_1 = MisilDeRobot(990,990,30,99)
        clasePrueba.calculoNuevasPosiociones([misil_1])
        # 0,866025404
        assert(misil_1.posicion_misil[0] == 999)
        assert(misil_1.posicion_misil[1] == 999)
        assert(misil_1.dist == 0)
        misil_2 = MisilDeRobot(10, 10, 210, 99)
        clasePrueba.calculoNuevasPosiociones([misil_2])
        assert(misil_2.posicion_misil[0] == 0)
        assert(misil_2.posicion_misil[1] == 0)
        assert(misil_2.dist == 0)

    def test_calculo_nueva_posicion_yendose_del_tablero(self):
        clasePrueba = Rondas()
        misil_1 = MisilDeRobot(990,990,30,350)
        clasePrueba.calculoNuevasPosiociones([misil_1])
        # 0,866025404
        assert(misil_1.posicion_misil[0] == 999)
        assert(misil_1.posicion_misil[1] == 999)
        assert(misil_1.dist == 0)

    def test_calculo_nueva_posicion_sin_dist(self):
        clasePrueba = Rondas()
        misil_1 = MisilDeRobot(10,20,30,50)
        misil_2 = MisilDeRobot(10,20,30,26)
        clasePrueba.calculoNuevasPosiociones([misil_1, misil_2])
        # 0,866025404
        position_x_misil_1 = 10 + round(50 * math.cos(math.radians(30)))
        position_x_misil_2 = 10 + round(26 * math.cos(math.radians(30)))
        assert(misil_1.posicion_misil[0] == position_x_misil_1)
        assert(misil_1.dist == 0)
        assert(misil_2.posicion_misil[0] == position_x_misil_2)
        assert(misil_2.dist == 0)

    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_disparar_nuevos_misiles(self, mockcodigo):
        mockcodigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.drive(self.get_direction()+20, 50)
        self.cannon(self.get_direction()+10, 300)
        """
        clasePrueba = Rondas()
        robot_1 = RobotEnJuego(111)
        robot_1.robot.posicion = (0,0)
        robot_1.robot.cannon(30, 500)
        robot_2 = RobotEnJuego(222)
        robot_2.robot.posicion = (500,500)
        robot_2.robot.cannon(30, 500)
        
        robot_3 = RobotEnJuego(222)
        robot_3.robot.posicion = (500,500)
        robot_3.robot.cannon(30, 500)
        robot_3.robot.rondasSinDisparar = 3
        
        listaRobots = [robot_1, robot_2,robot_3]
        listaMisiles = clasePrueba.dispararNuevosMisiles(listaRobots)
        assert(len(listaMisiles) == 2)
        assert(listaMisiles[0].posicion_misil[0] == 0)
        assert(listaMisiles[0].posicion_misil[1] == 0)
        assert(listaMisiles[1].posicion_misil[0] == 500)
        assert(listaMisiles[1].posicion_misil[1] == 500)

    def test_lista_de_misil_explotados(self):
        misil_1 = MisilDeRobot(0,0,30,0)
        misil_2 = MisilDeRobot(500,500,30,0)
        misil_3 = MisilDeRobot(700,700,30,450)
        lista_misiles = [misil_1, misil_2, misil_3]
        IUT = Rondas()
        coordenadas_de_explosion = IUT.listaDeMisilesExplotados(lista_misiles)
        assert(len(coordenadas_de_explosion) == 2)
        assert(coordenadas_de_explosion[0][0]==0)
        assert(coordenadas_de_explosion[0][1]==0)
        assert(coordenadas_de_explosion[1][0]==500)
        assert(coordenadas_de_explosion[1][1]==500)

    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_coalision_con_misiles(self, mockcodigo):
        mockcodigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.drive(self.get_direction()+20, 50)
        self.cannon(self.get_direction()+10, 300)
        """
        clasePrueba = Rondas()
        robot_1 = RobotEnJuego(111)
        robot_1.robot.posicion = (250,250)
        lista_robots = [robot_1]
        vida_antes_impacto = robot_1.robot.vida
        lista_coordenadas_explosion = [(250,253)]
        clasePrueba.coalisionConMisiles(lista_robots, lista_coordenadas_explosion)
        assert(robot_1.robot.vida == vida_antes_impacto-10)
        vida_antes_impacto = robot_1.robot.vida
        lista_coordenadas_explosion = [(250,265)]
        clasePrueba.coalisionConMisiles(lista_robots, lista_coordenadas_explosion)
        assert(robot_1.robot.vida == vida_antes_impacto-5)
        lista_coordenadas_explosion = [(250,280)]
        vida_antes_impacto = robot_1.robot.vida
        clasePrueba.coalisionConMisiles(lista_robots, lista_coordenadas_explosion)
        assert(robot_1.robot.vida == vida_antes_impacto-3)
        lista_coordenadas_explosion = [(250,280)]
        robot_1.robot.vida = 1
        vida_antes_impacto = robot_1.robot.vida
        clasePrueba.coalisionConMisiles(lista_robots, lista_coordenadas_explosion)
        assert(robot_1.robot.vida == 0)






