from unittest import TestCase, mock

from fun.Juego import Juego
from fun.RobotEnJuego import RobotEnJuego

class TestMockValue(TestCase):
   
    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_calculo_resultado(self,mock_stringRobot):
        mock_stringRobot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass"""

        robot_1_test = RobotEnJuego(1)
        robot_2_test = RobotEnJuego(1)
        robot_3_test = RobotEnJuego(1)
        robot_4_test = RobotEnJuego(1)

        robot_1_test.rondas_vivos = 5
        robot_2_test.rondas_vivos = 4
        robot_3_test.rondas_vivos = 3
        robot_4_test.rondas_vivos = 2

        lista_robot_test= [robot_1_test,robot_2_test,robot_3_test,robot_4_test]
        juego = Juego()
        juego.calcularResultado(lista_robot_test,4)

        self.assertEqual(robot_1_test.posicion_fin_del_juego,1)
        self.assertEqual(robot_2_test.posicion_fin_del_juego,2)
        self.assertEqual(robot_3_test.posicion_fin_del_juego,3)
        self.assertEqual(robot_4_test.posicion_fin_del_juego,4)


    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_calculo_resultado_empate(self,mock_stringRobot):
        mock_stringRobot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass"""

        robot_1_test = RobotEnJuego(1)
        robot_2_test = RobotEnJuego(2)
        robot_3_test = RobotEnJuego(3)
        robot_4_test = RobotEnJuego(4)

        robot_1_test.rondas_vivos = 5
        robot_2_test.rondas_vivos = 5
        robot_3_test.rondas_vivos = 3
        robot_4_test.rondas_vivos = 3

        lista_robot_test= [robot_1_test,robot_2_test,robot_3_test,robot_4_test]
        juego = Juego()
        juego.calcularResultado(lista_robot_test,4)

        self.assertEqual(robot_1_test.posicion_fin_del_juego,1)
        self.assertEqual(robot_2_test.posicion_fin_del_juego,1)
        self.assertEqual(robot_3_test.posicion_fin_del_juego,3)
        self.assertEqual(robot_4_test.posicion_fin_del_juego,3)

    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_termino_juego(self,mock_stringRobot):
        mock_stringRobot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass"""

        robot_1_test = RobotEnJuego(1)
        robot_2_test = RobotEnJuego(2)
        robot_3_test = RobotEnJuego(3)
        robot_4_test = RobotEnJuego(4)

        lista_robots_test = [robot_1_test,robot_2_test,robot_3_test,robot_4_test]
        juego = Juego()
        resultado_test = juego.terminoJuego(lista_robots_test)
        assert(not resultado_test)

        robot_1_test.robot.vida = 0
        robot_2_test.robot.vida = 0
        robot_3_test.robot.vida = 0
        resultado_test = juego.terminoJuego(lista_robots_test)
        assert(resultado_test)
