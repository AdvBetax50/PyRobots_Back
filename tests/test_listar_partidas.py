from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.ListarPartidas import ListarPartidas

IUT = ListarPartidas('example.sqlite')

class TestMockValue(TestCase):
 
    # Lista de partidas vacias.
    @mock.patch("fun.Sesion.SesionDB.consultarCantidadUnidos")
    @mock.patch("fun.Sesion.SesionDB.listarPartidasDB")
    def test_partidas_vacias(self, mock_partida, mock_cantidad):
        mock_partida.return_value = []
        mock_cantidad.return_value = 2
        response = IUT.listarPartidasDisponibles("Admin")
        self.assertEqual(response, [])

    # Lista con dos partidas.
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.tieneContrasena")
    @mock.patch("fun.Sesion.SesionDB.consultarCreadorPartida")
    @mock.patch("fun.Sesion.SesionDB.consultarCantidadUnidos")
    @mock.patch("fun.Sesion.SesionDB.listarPartidasDB")
    def test_partidas_dobles(self, mock_partida, mock_cantidad, 
            mock_creador, mock_contrasena, mock_unido):
        mock_partida.return_value = [
            {"id":2,
            "nombre":"partida1",
            "estado":"DISPONIBLE",
            "jugadoresMax": 4,
            "jugadoresMin": 3,
            "juegosTotales": 100,
            "rondasTotales": 200,
            "terminado":False},
            {"id":4,
            "nombre":"partida2",
            "estado":"DISPONIBLE",
            "jugadoresMax": 3,
            "jugadoresMin": 2,
            "juegosTotales": 50,
            "rondasTotales": 1000,
            "terminado":False}]
        mock_cantidad.return_value = 2
        mock_creador.return_value = True
        mock_contrasena.return_value = False
        mock_unido.return_value = False

        response = IUT.listarPartidasDisponibles("Admin")
        self.assertEqual(response, [
            {'id': 2, 
            'nombre': 'partida1', 
            'jugadoresMax': 4, 
            'jugadoresMin': 3, 
            'juegosTotales': 100, 
            'rondasTotales': 200,
            'terminado': False,
            'usuariosUnidos': 2,
            'creador': True,
            'contrasena': False,
            'estaUnido': False},
            {'id': 4, 
            'nombre': 'partida2', 
            'jugadoresMax': 3, 
            'jugadoresMin': 2, 
            'juegosTotales': 50, 
            'rondasTotales': 1000,
            'terminado': False,
            'usuariosUnidos': 2,
            'creador': True,
            'contrasena': False,
            'estaUnido': False}])
