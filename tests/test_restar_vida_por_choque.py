from unittest import TestCase, mock

from fun.RobotEnJuego import RobotEnJuego

class TestMockValue(TestCase):
   
    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_SiempreSeResteVidaEnCasosAfirmativosYLaVidaNuncaNegatica(self,mock_stringRobot):
        mock_stringRobot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.point_scanner(45,10)
        """
    
        robotEnJuego1 = RobotEnJuego(1)
        robotEnJuego2 = RobotEnJuego(2)
        lista_robots = [robotEnJuego1, robotEnJuego2]
        vida_restante = 100
        robotEnJuego1.robot.posicion  = (0,0)
        robotEnJuego2.robot.posicion  = (0,0)
        
        for _ in range(1,54):
            RobotEnJuego.infligirDañoPorChoqueEntreRobots(lista_robots)
            vida_restante = 0 if vida_restante <= 2 else vida_restante - 2
            self.assertEqual(robotEnJuego1.robot.vida, vida_restante)
            self.assertEqual(robotEnJuego2.robot.vida, vida_restante)
                
    @mock.patch("fun.Sesion.SesionDB.stringRobot") 
    def test_choque_de_robots(self,mock_stringRobot):
        mock_stringRobot.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        x, y = self.get_position()
        self.point_scanner(45,10)
        """
    
        robotEnJuego1 = RobotEnJuego(1)
        robotEnJuego2 = RobotEnJuego(2)
        lista_robots = [robotEnJuego1, robotEnJuego2]
        robotEnJuego1.robot.posicion = (0,10)
        robotEnJuego2.robot.posicion = (0,8)

        robotEnJuego1.robot.vida = 100 
        robotEnJuego2.robot.vida = 100   
        RobotEnJuego.infligirDañoPorChoqueEntreRobots(lista_robots)
        self.assertEqual(robotEnJuego1.robot.vida, 98)
        self.assertEqual(robotEnJuego2.robot.vida, 98)

        robotEnJuego1.robot.vida = 50
        robotEnJuego2.robot.vida = 1
        RobotEnJuego.infligirDañoPorChoqueEntreRobots(lista_robots)
        self.assertEqual(robotEnJuego1.robot.vida, 48)
        self.assertEqual(robotEnJuego2.robot.vida, 0)
        
        robotEnJuego1.robot.vida = 50
        robotEnJuego2.robot.vida = 0
        RobotEnJuego.infligirDañoPorChoqueEntreRobots(lista_robots)
        self.assertEqual(robotEnJuego1.robot.vida, 50)
        self.assertEqual(robotEnJuego2.robot.vida, 0)