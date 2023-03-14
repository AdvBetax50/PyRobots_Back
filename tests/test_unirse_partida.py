from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.UnirsePartida import UnirsePartida

IUT = UnirsePartida('example.sqlite')

class TestMockValue(TestCase): 

    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_incorrecto(self, mock_usuario):
        mock_usuario.return_value = False
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":None})
        self.assertEqual(response, "USUARIO_INVALIDO")
    
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida_no_existe(self, mock_usuario, mock_partida):
        mock_usuario.return_value = True
        mock_partida.return_value = False
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":None})
        self.assertEqual(response, "PARTIDA_INVALIDA")
    
    @mock.patch("fun.Sesion.SesionDB.estaLlenaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida_llena(self, mock_usuario, mock_partida,
            mock_llena):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_llena.return_value = True
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, "PARTIDA_LLENA")

    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.estaLlenaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_ya_unido(self, mock_usuario, mock_partida,
            mock_llena, mock_unido):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_llena.return_value = False
        mock_unido.return_value = True
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, "USUARIO_YA_UNIDO")

    @mock.patch("fun.Sesion.SesionDB.existeRobotUsuario")
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.estaLlenaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_robot_no_existe(self, mock_usuario, mock_partida,
            mock_llena, mock_unido, mock_robot):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_llena.return_value = False
        mock_unido.return_value = False
        mock_robot.return_value = False
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, "ROBOT_INVALIDO")

    @mock.patch("fun.Sesion.SesionDB.esCorrectaContrasena")
    @mock.patch("fun.Sesion.SesionDB.tieneContrasena")
    @mock.patch("fun.Sesion.SesionDB.existeRobotUsuario")
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.estaLlenaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_contrasena_incorrecta(self, mock_usuario, mock_partida,
            mock_llena, mock_unido, mock_robot, mock_tiene_cont, 
            mock_es_corr):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_llena.return_value = False
        mock_unido.return_value = False
        mock_robot.return_value = True
        mock_tiene_cont.return_value = True
        mock_es_corr.return_value = False
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, "CONTRASENA_INVALIDA")

    @mock.patch("fun.ConexionWS.ConexionWS.actualizarDatosWS")
    @mock.patch("fun.Sesion.SesionDB.consultarCantidadUnidos")
    @mock.patch("fun.Sesion.SesionDB.registrarUsuarioEnPartida")
    @mock.patch("fun.Sesion.SesionDB.esCorrectaContrasena")
    @mock.patch("fun.Sesion.SesionDB.tieneContrasena")
    @mock.patch("fun.Sesion.SesionDB.existeRobotUsuario")
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.estaLlenaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_unirse_exitoso(self, mock_usuario, mock_partida,
            mock_llena, mock_unido, mock_robot, mock_tiene_cont,
            mock_es_corr, mock_registro, mock_unidos, mock_fun):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_llena.return_value = False
        mock_unido.return_value = False
        mock_robot.return_value = True
        mock_tiene_cont.return_value = True
        mock_es_corr.return_value = True
        mock_registro.return_value = True
        mock_unidos.return_value = 2
        mock_fun.return_value = True
        response = IUT.unirNuevoUsuario({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, {'websocket': 'ws://localhost:5000/ws/unirse/1'})