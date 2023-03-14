from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.AbandonarPartida import AbandonarPartida

IUT = AbandonarPartida('example.sqlite')

class TestMockValue(TestCase): 

    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_incorrecto(self, mock_usuario):
        mock_usuario.return_value = False
        response = IUT.quitarUsuarioDePartida({
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
        response = IUT.quitarUsuarioDePartida({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":None})
        self.assertEqual(response, "PARTIDA_INVALIDA")

    @mock.patch("fun.Sesion.SesionDB.esCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_es_creador(self, mock_usuario, mock_partida,
            mock_creador):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_creador.return_value = True
        response = IUT.quitarUsuarioDePartida({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, "USUARIO_CREADOR")

    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.esCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_no_unido(self, mock_usuario, mock_partida,
            mock_creador, mock_unido):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_creador.return_value = False
        mock_unido.return_value = False
        response = IUT.quitarUsuarioDePartida({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, "USUARIO_NO_UNIDO")

    @mock.patch("fun.ConexionWS.ConexionWS.actualizarDatosWS")
    @mock.patch("fun.Sesion.SesionDB.consultarCantidadUnidos")
    @mock.patch("fun.Sesion.SesionDB.borrarUsuarioDePartida")
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.esCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_abandonar_exitoso(self, mock_usuario, mock_partida,
            mock_creador, mock_unido, mock_registro, mock_unidos, _):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_creador.return_value = False
        mock_unido.return_value = True
        mock_registro.return_value = True
        mock_unidos.return_value = 1
        response = IUT.quitarUsuarioDePartida({
            "partida_id":1,
            "nombre_us":"Admin",
            "robot_id":1,
            "contrasena":''})
        self.assertEqual(response, {'exito': True})
