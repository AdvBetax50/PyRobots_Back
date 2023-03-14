from unittest import TestCase, mock

from fun.RobotEnJuego import RobotEnJuego

class TestMockValue(TestCase):
    
    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_robot_choque_pared(self, mockcodigo):
        mockcodigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.point_scanner(0,10)

        """
        robot_1 = RobotEnJuego(111)
        robot_1.robot.posicion = (998,998)
        robot_2 = RobotEnJuego(222)
        robot_2.robot.posicion = (998,998)
        robot_3 = RobotEnJuego(333)
        robot_3.robot.posicion = (2,2)
        robot_4 = RobotEnJuego(444)
        robot_4.robot.posicion = (2,2)

        robot_1.robot.drive(0, 49)
        robot_2.robot.drive(90, 49)
        robot_3.robot.drive(270, 49)
        robot_4.robot.drive(180, 49)


        RobotEnJuego.moverRobot(robot_1)
        RobotEnJuego.moverRobot(robot_2)
        RobotEnJuego.moverRobot(robot_3)
        RobotEnJuego.moverRobot(robot_4)

        assert(robot_1.robot.vida == 98)
        assert(robot_2.robot.vida == 98)
        assert(robot_3.robot.vida == 98)
        assert(robot_4.robot.vida == 98)


