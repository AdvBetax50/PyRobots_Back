from unittest import TestCase, mock

from fun.Partida import Partida

IUT = Partida('example.sqlite')

class TestMockValue(TestCase):

    @mock.patch("fun.Sesion.SesionDB.registrarResultados")
    @mock.patch("fun.Juego.Juego.iniciarJuego")
    @mock.patch("fun.Sesion.SesionDB.obtenerDatosPartidas")
    def test_partida_sin_empate(self, mock_datos, mock_juego, mock_registro): 
        mock_datos.return_value = {"rondas":100,
            "juegos":10,
            "robots":[1,2]}
        mock_juego.return_value = {
            "simulacion":[], 
            "resultado":[{
                "id":1,
                "posicion":1},{
                "id":2,
                "posicion":2}]}
        mock_registro.return_value = True
        config = {
            "nombre_us": "Admin",
            "partida_id": 1}
        response = IUT.ejecutarPartida(config)
        self.assertEqual(response[0]["robot_resultado"], "Ganador")
        self.assertEqual(response[0]["juegos_ganados"], 10)
        self.assertEqual(response[0]["juegos_perdidos"], 0)
        self.assertEqual(response[0]["juegos_empatados"], 0)
        self.assertEqual(response[1]["robot_resultado"], "Perdedor")
        self.assertEqual(response[1]["juegos_ganados"], 0)
        self.assertEqual(response[1]["juegos_perdidos"], 10)
        self.assertEqual(response[1]["juegos_empatados"], 0)
    
    @mock.patch("fun.Sesion.SesionDB.registrarResultados")
    @mock.patch("fun.Juego.Juego.iniciarJuego")
    @mock.patch("fun.Sesion.SesionDB.obtenerDatosPartidas")
    def test_partida_con_empate(self, mock_datos, mock_juego, mock_registro): 
        mock_datos.return_value = {"rondas":100,
            "juegos":10,
            "robots":[1,2,3]}
        mock_juego.return_value = {
            "simulacion":[], 
            "resultado":[{
                "id":1,
                "posicion":1},{
                "id":2,
                "posicion":1},{
                "id":3,
                "posicion":3}]}
        mock_registro.return_value = True
        config = {
            "nombre_us": "Admin",
            "partida_id": 1}
        response = IUT.ejecutarPartida(config)
        self.assertEqual(response[0]["robot_resultado"], "Empate")
        self.assertEqual(response[0]["juegos_ganados"], 0)
        self.assertEqual(response[0]["juegos_perdidos"], 0)
        self.assertEqual(response[0]["juegos_empatados"], 10)
        self.assertEqual(response[1]["robot_resultado"], "Empate")
        self.assertEqual(response[1]["juegos_ganados"], 0)
        self.assertEqual(response[1]["juegos_perdidos"], 0)
        self.assertEqual(response[1]["juegos_empatados"], 10)
        self.assertEqual(response[2]["robot_resultado"], "Perdedor")
        self.assertEqual(response[2]["juegos_ganados"], 0)
        self.assertEqual(response[2]["juegos_perdidos"], 10)
        self.assertEqual(response[2]["juegos_empatados"], 0)
