from unittest import TestCase, mock
import base64

import sys
sys.path.append("..")
from fun.Rondas import Rondas
from fun.RobotEnJuego import RobotEnJuego


class TestMockValue(TestCase):
    
    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_time_out_robot_loop_infinito(self, mock_codigo_robot):
        mock_codigo_robot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        while 1:
            pass

        """

        newRonda = Rondas()
        robot_1 = RobotEnJuego(111)
        robot_2 = RobotEnJuego(112)
        lista_robot = {"robots" : [robot_1, robot_2], "misiles":[]}
        
        estadoDeLaRonda = newRonda.avanzarRonda(lista_robot)

        print(estadoDeLaRonda["robots"])

        assert(estadoDeLaRonda["robots"][0]["estado"] == 0)
        assert(estadoDeLaRonda["robots"][1]["estado"] == 0)

    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_time_out_robot_loop_finito(self, mock_codigo_robot):
        mock_codigo_robot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.point_scanner(0,10)
        """


        newRonda = Rondas()
        robot_1 = RobotEnJuego(111)
        robot_2 = RobotEnJuego(112)
        #Cambiamos de posicion para que no haya coalisión entre los robots
        robot_2.robot.posicion = (100,100)
        lista_robot = {"robots" : [robot_1, robot_2], "misiles":[]}
        
        estadoDeLaRonda = newRonda.avanzarRonda(lista_robot)

        print(estadoDeLaRonda["robots"])

        assert(estadoDeLaRonda["robots"][0]["estado"] == 100)
        assert(estadoDeLaRonda["robots"][1]["estado"] == 100)


