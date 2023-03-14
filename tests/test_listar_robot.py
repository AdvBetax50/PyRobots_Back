from unittest import TestCase, mock
import base64

import sys
sys.path.append("..")
from fun.ListarRobots import ListarRobots

IUT = ListarRobots('example.sqlite')

lista_robot = [
    {"id":1, "nombre": "rob1", "avatar":"avatar1"},
    {"id":2, "nombre": "rob2", "avatar":"avatar2"}]

class TestMockValue(TestCase):
    
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_listar_robot_vacio(self, mock_usuario):
        mock_usuario.return_value = False
        response = IUT.listarRobots("Admin")
        self.assertEqual(response, [])

    @mock.patch("fun.Sesion.SesionDB.listarRobotDB")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_listar_robot_varios(self, mock_usuario, mock_listar_robot):
        mock_usuario.return_value = True
        mock_listar_robot.return_value =lista_robot
        response = IUT.listarRobots("Admin")
        self.assertEqual(response, lista_robot)
    
    @mock.patch("fun.Sesion.SesionDB.obtenerAvatarRobotDB")
    def test_robot_avatar(self, mock_avatar):
        mock_avatar.return_value = base64.b64encode(b"avatar")
        response = IUT.obtenerAvatarRobot(1)
        self.assertEqual(response, base64.b64encode(b"avatar"))