from unittest import TestCase, mock

from fun.RobotEnJuego import RobotEnJuego

class TestMockValue(TestCase):
   
    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_retornos_de_la_calse_robot(self, mock_codigo):
        mock_codigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass
        """ 
        robotEnJuego = RobotEnJuego(1)
        self.assertEqual(robotEnJuego.robot.get_damage(), 100)
        self.assertEqual(robotEnJuego.robot.get_velocity(), 0)
        self.assertEqual(robotEnJuego.robot.get_direction(), 0)
        self.assertEqual(robotEnJuego.robot.get_position(), (0,0))
    
    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_robot_defectuoso(self, mock_codigo):
        mock_codigo.return_value = """
ROBOT DEFECTUOSO
        """ 
        robotEnJuego = RobotEnJuego(1)
        self.assertEqual(robotEnJuego.robot.vida, 0)