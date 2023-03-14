from unittest import TestCase, mock

from fun.RobotEnJuego import RobotEnJuego
from fun.Juego import Juego

class TestMockValue(TestCase):

    @mock.patch("fun.Rondas.Rondas.avanzarRonda")
    @mock.patch("fun.Rondas.Rondas.iniciarRonda")
    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_iniciar_juego_sin_muertes(self,mock_codigo, mock_iniciar, mock_avanzar):
        mock_codigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass"""
        robot_1 = RobotEnJuego(1)
        robot_2 = RobotEnJuego(2)
        mock_iniciar.return_value = [robot_1, robot_2]
        mock_avanzar.return_value = {"robots" : [
            {"id":1,"estado":90},
            {"id":2,"estado":80}],
            "misiles" : []}
        configuracion = {"rondas": 100, "robots": [1,2]}
        juego = Juego()
        response = juego.iniciarJuego(configuracion)
        self.assertEqual(len(response["simulacion"]), 100)
        self.assertEqual(response["simulacion"][0]["robots"][0]["estado"], 90)
        self.assertEqual(response["simulacion"][99]["robots"][0]["estado"], 90)
        self.assertEqual(response["simulacion"][0]["robots"][1]["estado"], 80)
        self.assertEqual(response["simulacion"][99]["robots"][1]["estado"], 80)

    @mock.patch("fun.Rondas.Rondas.avanzarRonda")
    @mock.patch("fun.Rondas.Rondas.iniciarRonda")
    @mock.patch("fun.Sesion.SesionDB.stringRobot")
    def test_iniciar_juego_con_muertes(self,mock_codigo, mock_iniciar, mock_avanzar):
        mock_codigo.return_value = """
class SuperClase(Robot):
    def initialize(self):
        pass
    def responds(self):
        pass"""
        robot_1 = RobotEnJuego(1)
        robot_2 = RobotEnJuego(2)
        robot_1.robot.vida=0
        robot_1.robot.vida=0
        mock_iniciar.return_value = [robot_1, robot_2]
        mock_avanzar.return_value = {"robots" : [
            {"id":1,"estado":0},
            {"id":2,"estado":0}],
            "misiles" : []}
        configuracion = {"rondas": 100, "robots": [1,2]}
        juego = Juego()
        response = juego.iniciarJuego(configuracion)
        self.assertEqual(len(response["simulacion"]), 1)
        self.assertEqual(response["simulacion"][0]["robots"][0]["estado"], 0)
        self.assertEqual(response["simulacion"][0]["robots"][1]["estado"], 0)