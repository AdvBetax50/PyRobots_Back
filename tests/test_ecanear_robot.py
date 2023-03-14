from unittest import TestCase, mock

from fun.RobotEnJuego import RobotEnJuego

class TestMockValue(TestCase):

    def test_calculo_de_angulo(self):
        IUT = RobotEnJuego(1)
        punto1 = (0,0)
        punto2 = (0,10)
        punto3 = (0,0)
        punto4 = (10,0)
        punto5 = (10,0)
        punto6 = (0,0)
        resultado_angulo1 = IUT.calcularAngulo(punto1,punto2)
        resultado_angulo2 = IUT.calcularAngulo(punto3,punto4)
        resultado_angulo3 = IUT.calcularAngulo(punto5,punto6)
        assert(resultado_angulo1 == 90)
        assert(resultado_angulo2 == 0)
        assert(resultado_angulo3 == 180)

    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_robot_escaneado(self, mockcodigo):
        mockcodigo.return_value= """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.point_scanner(45,10)

        """
        robot_1 = RobotEnJuego(111)
        robot_1.robot.posicion = (0,0)
        robot_2 = RobotEnJuego(222)
        robot_2.robot.posicion = (4,3)
        lista_robot=[robot_1,robot_2]
        robot_1.robot.point_scanner(45,20)
        robot_2.robot.point_scanner(195,-20)
        robot_1.escanear(lista_robot)
        robot_2.escanear(lista_robot)
        assert(robot_1.robot.distanciaScaneo == 5)
        assert(robot_2.robot.distanciaScaneo == 0)


    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_robot_distancia_escaneada(self, mockcodigo):
        mockcodigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.point_scanner(0,10)

        """
        robot_1 = RobotEnJuego(111)
        robot_1.robot.posicion = (100,500)
        robot_2 = RobotEnJuego(222)
        robot_2.robot.posicion = (900,500)
        lista_robot = [robot_1,robot_2]
        robot_1.robot.point_scanner(5,10)
        robot_2.robot.point_scanner(355,10)
        robot_1.escanear(lista_robot)
        robot_2.escanear(lista_robot)
        assert(robot_1.robot.distanciaScaneo == 800 )
        assert(robot_2.robot.distanciaScaneo == 0 )
        robot_2.robot.vida = 0
        robot_1.escanear(lista_robot)
        assert(robot_1.robot.distanciaScaneo == 0 )