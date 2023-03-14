from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.RegistrarRobot import RegistrarRobot

IUT = RegistrarRobot('example.sqlite') 

robot_sin_avatar = {
    "nombre_usuario": "Admin",
    "nombre": "bot",
    "avatar": None,
    "codigo": "codigo"}

robot_con_avatar = {
    "nombre_usuario": "Admin",
    "nombre": "bot",
    "avatar": "imagen",
    "codigo": "codigo"}

class TestMockValue(TestCase):

    # Usuario no existe en la base de datos.
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_existe_nombre(self, mock_response):
        mock_response.return_value = False
        response = IUT.registrarRobot(robot_con_avatar)
        self.assertEqual(response, {"result":"Usuario_No_Registrado"})
    
    # Registro exitoso sin avatar
    @mock.patch("fun.Sesion.SesionDB.registrarRobotSinAvatar")
    @mock.patch("fun.Sesion.SesionDB.obtenerIdUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_registro_robot_sin_avatar(self, mock_nombre, mock_id, mock_registro):
        mock_nombre.return_value = True
        mock_id.return_value = 1
        mock_registro.return_value = 2
        response = IUT.registrarRobot(robot_sin_avatar)
        self.assertEqual(response, {"id":2})
    
    # Registro exitoso con avatar
    @mock.patch("fun.Sesion.SesionDB.registrarRobotConAvatar")
    @mock.patch("fun.Sesion.SesionDB.obtenerIdUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_registro_robot_con_avatar(self, mock_nombre, mock_id, mock_registro):
        mock_nombre.return_value = True
        mock_id.return_value = 1
        mock_registro.return_value = 2
        response = IUT.registrarRobot(robot_con_avatar)
        self.assertEqual(response, {"id":2})