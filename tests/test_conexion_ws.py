from unittest import TestCase, mock
import requests

import sys
sys.path.append("..")
from fun.ConexionWS import ConexionWS

IUT = ConexionWS()

class TestMockValue(TestCase): 

    @mock.patch("requests.post")
    def test_enviar_mensaje_exepcion(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError()
        response = IUT.actualizarDatosWS(1,1)
        self.assertEqual(response, False)
    
    @mock.patch("requests.post")
    def test_enviar_mensaje_correcto(self, mock_request):
        mock_request.json.return_value = True
        response = IUT.actualizarDatosWS(1,1)
        self.assertEqual(response, True)

    @mock.patch("requests.post")
    def test_actualizar_resultados_exepcion(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError()
        response = IUT.actualizarResultadosWS(1,1)
        self.assertEqual(response, False)
    
    @mock.patch("requests.post")
    def test_actualizar_resultados_correcto(self, mock_request):
        mock_request.json.return_value = True
        response = IUT.actualizarResultadosWS(1,1)
        self.assertEqual(response, True)