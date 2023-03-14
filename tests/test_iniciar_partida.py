from unittest import TestCase, mock

from fun.IniciarPartida import PartidaIniciar

IUT = PartidaIniciar('example.sqlite')

class TestMockValue(TestCase): 

    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_incorrecto(self, mock_usuario):
        mock_usuario.return_value = False
        response = IUT.iniciarPartida({
            "nombre_us": "Admin",
            "partida_id": 1})
        self.assertEqual(response, "USUARIO_INVALIDO")
    
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida_incorrecta(self, mock_usuario, 
            mock_partida):
        mock_usuario.return_value = True
        mock_partida.return_value = False
        response = IUT.iniciarPartida({
            "nombre_us": "Admin",
            "partida_id": 1})
        self.assertEqual(response, "PARTIDA_INVALIDA")
    
    @mock.patch("fun.Sesion.SesionDB.estaTerminadaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida_terminada(self, mock_usuario, 
            mock_partida, mock_terminada):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_terminada.return_value = True
        response = IUT.iniciarPartida({
            "nombre_us": "Admin",
            "partida_id": 1})
        self.assertEqual(response, "PARTIDA_TERMINADA")
    
    @mock.patch("fun.Sesion.SesionDB.esCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.estaTerminadaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_no_creador(self, mock_usuario, 
            mock_partida, mock_terminada, mock_creador):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_terminada.return_value = False
        mock_creador.return_value = False
        response = IUT.iniciarPartida({
            "nombre_us": "Admin",
            "partida_id": 1})
        self.assertEqual(response, "USUARIO_NO_CREADOR")
    
    @mock.patch("fun.Sesion.SesionDB.esCantidadUsValida")
    @mock.patch("fun.Sesion.SesionDB.esCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.estaTerminadaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_faltan_jugadores(self, mock_usuario, 
            mock_partida, mock_terminada, mock_creador,
            mock_unidos):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_terminada.return_value = False
        mock_creador.return_value = True
        mock_unidos.return_value = False
        response = IUT.iniciarPartida({
            "nombre_us": "Admin",
            "partida_id": 1})
        self.assertEqual(response, "FALTAN_JUGADORES")

    @mock.patch("fun.ConexionWS.ConexionWS.actualizarResultadosWS")
    @mock.patch("fun.Partida.Partida.ejecutarPartida")
    @mock.patch("fun.Sesion.SesionDB.esCantidadUsValida")
    @mock.patch("fun.Sesion.SesionDB.esCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.estaTerminadaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida_correctamente(self, mock_usuario, 
            mock_partida, mock_terminada, mock_creador,
            mock_unidos, mock_iniciar, mock_ws):
        mock_usuario.return_value = True
        mock_partida.return_value = True
        mock_terminada.return_value = False
        mock_creador.return_value = True
        mock_unidos.return_value = True
        mock_iniciar.return_value = {"info_partida"}
        mock_ws.return_value = True
        response = IUT.iniciarPartida({
            "nombre_us": "Admin",
            "partida_id": 1})
        self.assertEqual(response, {"exito":True})