from unittest import TestCase, mock

from fun.Rondas import Rondas
from fun.RobotEnJuego import RobotEnJuego

class TestMockValue(TestCase):
    
    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_ronda_inicial(self, mock_codigo):
        mock_codigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass """ 
        configuracion = {"rondas": 100, "robots": [1,2]}
        IUT = Rondas()
        response = IUT.iniciarRonda(configuracion)
        self.assertEqual(response[0].robot.vida, 100)
        self.assertEqual(response[1].robot.vida, 100)
        mock_codigo.return_value = """
class SuperClase(Robot):
    def responds(self):
        pass """
        response = IUT.iniciarRonda(configuracion)
        self.assertEqual(response[0].robot.vida, 0)
        self.assertEqual(response[1].robot.vida, 0)

    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_ronda_avanzar_con_robots_defectuosos(self, mock_codigo):
        mock_codigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass""" 
        robot_1 = RobotEnJuego(1)
        robot_2 = RobotEnJuego(2)
        ronda_actual = {"robots":[robot_1,robot_2],"misiles":[]}
        IUT = Rondas()
        response = IUT.avanzarRonda(ronda_actual)
        self.assertEqual(response, {
            "robots" : [{'canon': 0,
                'estado': 0,
                'id': 1,
                'nombre': '',
                'pos_x': 0,
                'pos_y': 0,
                'velocidad': 0,
                'vision': 0},
                {'canon': 0,
                'estado': 0,
                'id': 2,
                'nombre': '',
                'pos_x': 0,
                'pos_y': 0,
                'velocidad': 0,
                'vision': 0}], 
            "misiles" : []})
    
    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_ronda_avanzar_con_robot_que_disparan(self, mock_codigo):
        mock_codigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        self.point_scanner(90, 15)
        scn = self.scanned()
        self.drive(scn, 50)
        self.cannon(90, 100)""" 
        robot_1 = RobotEnJuego(1)
        robot_2 = RobotEnJuego(2)
        ronda_actual = {"robots":[robot_1,robot_2],"misiles":[]}
        IUT = Rondas()
        response = IUT.avanzarRonda(ronda_actual)
        self.assertEqual(len(response["misiles"]), 2)
