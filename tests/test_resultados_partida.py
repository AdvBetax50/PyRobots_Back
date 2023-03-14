from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.ResultadosPartida import ResultadosPartida

IUT = ResultadosPartida('example.sqlite')

class TestMockValue(TestCase): 
    
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_(self, mock_usuario, mock_unido):
        mock_usuario.return_value = False
        mock_unido.return_value = True
        response = IUT.obtenerResultados({
            "partida_id":1,
            "nombre_us":"Admin"})
        self.assertEqual(response, "USUARIO_INVALIDO")
        mock_usuario.return_value = True
        mock_unido.return_value = False
        response = IUT.obtenerResultados({
            "partida_id":1,
            "nombre_us":"Admin"})
        self.assertEqual(response, "USUARIO_INVALIDO")
    
    @mock.patch("fun.Sesion.SesionDB.estaTerminadaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida(self, mock_usuario, mock_unido,
                mock_partida, mock_terminada):
        mock_usuario.return_value = True
        mock_unido.return_value = True
        mock_partida.return_value = False
        mock_terminada.return_value = True
        response = IUT.obtenerResultados({
            "partida_id":1,
            "nombre_us":"Admin"})
        self.assertEqual(response, "PARTIDA_INVALIDA") 
        mock_partida.return_value = True
        mock_terminada.return_value = False
        response = IUT.obtenerResultados({
            "partida_id":1,
            "nombre_us":"Admin"})
        self.assertEqual(response, "PARTIDA_INVALIDA")

    @mock.patch("fun.Sesion.SesionDB.obtenerResultadosPartida")
    @mock.patch("fun.Sesion.SesionDB.estaTerminadaPartida")
    @mock.patch("fun.Sesion.SesionDB.existePartida")
    @mock.patch("fun.Sesion.SesionDB.estaUnido")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_partida_resultados(self, mock_usuario, mock_unido,
                mock_partida, mock_terminada, mock_resultados):
        mock_usuario.return_value = True
        mock_unido.return_value = True
        mock_partida.return_value = True
        mock_terminada.return_value = True
        mock_resultados.return_value = [{
            "robotId":1,
            "resultado":"Ganador",
            "ganados": 50,
            "perdidos": 40,
            "empatados": 10}]
        response = IUT.obtenerResultados({
            "partida_id":1,
            "nombre_us":"Admin"})
        self.assertEqual(response, [{
            "robotId":1,
            "resultado":"Ganador",
            "ganados": 50,
            "perdidos": 40,
            "empatados": 10}]) 