from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.RegistrarPartidaCreada import RegistrarPartida

IUT = RegistrarPartida('example.sqlite')

class TestMockValue(TestCase):
    
    def test_jugadores_minimos(self):
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 4, 
            "jugadoresMin": 0, 
            "juegosTotales": 10, 
            "rondasTotales": 10,
            "robotUsuario":1, 
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {"result":"JUGADORES_MIN_INVALIDO"})

    def test_jugadores_maximos(self):
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 5, 
            "jugadoresMin": 2, 
            "juegosTotales": 10, 
            "rondasTotales": 10,
            "robotUsuario":1, 
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {"result":"JUGADORES_MAX_INVALIDO"})
        
    def test_juegos_totales(self):
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 4, 
            "jugadoresMin": 2, 
            "juegosTotales": 1000, 
            "rondasTotales": 10,
            "robotUsuario":1,
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {"result":"JUGOS_TOATALES_INVALIDO"})
  
    def test_rondas_totales(self):
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 4, 
            "jugadoresMin": 2, 
            "juegosTotales": 100, 
            "rondasTotales": 100000,
            "robotUsuario":1,
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {"result":"RONDAS_TOTALES_INVALIDO"})
    
    # Admin ya existe en la base de datos.
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_existe_nombre(self, mock_response):
        mock_response.return_value = False
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 4, 
            "jugadoresMin": 2, 
            "juegosTotales": 10, 
            "rondasTotales": 10,
            "robotUsuario":1,
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {"result":"USUARIO_INVALIDO"})

    # El robot no existe en la base de datos.
    @mock.patch("fun.Sesion.SesionDB.existeRobotUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_no_existe_robot(self, mock_usuario, mock_robot):
        mock_usuario.return_value = True
        mock_robot.return_value = False
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 4, 
            "jugadoresMin": 2, 
            "juegosTotales": 10, 
            "rondasTotales": 10,
            "robotUsuario":1, 
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {"result":"ROBOT_INVALIDO"})

    # Registro exitoso de la partida.
    @mock.patch("fun.Sesion.SesionDB.registrarPartidaCreadaDB")
    @mock.patch("fun.Sesion.SesionDB.existeRobotUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_registrar_partida(self, mock_nombre,mock_robot, mock_registrar):
        mock_nombre.return_value = True
        mock_robot.return_value = True
        mock_registrar.return_value = 1
        response = IUT.registrarPartidaCreada({
            "nombre": "nombre",
            "jugadoresMax": 4, 
            "jugadoresMin": 2, 
            "juegosTotales": 10, 
            "rondasTotales": 10,
            "robotUsuario":1,
            "contrasena": None, 
            "nombreUsuario": "Admin"})
        self.assertEqual(response, {
            "websocket":"ws://localhost:5000/ws/unirse/1"})
