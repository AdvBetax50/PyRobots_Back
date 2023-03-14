import requests 

class ConexionWS:

    def actualizarDatosWS(self, partida_id, unidos):
        url = "http://localhost:5000/ws/cantidad/"
        datos = {'partida':partida_id, 'unidos':unidos}
        try:
            respuesta = requests.post(url = url, params = datos)
            respuesta.json()
            return True
        except:
            print("Error al comunicarse con el websocket")
            return False
        
    def actualizarResultadosWS(self, partida_id, resultado):
        url = "http://localhost:5000/ws/resultado/"
        datos = {'partida':partida_id, 'resultado': resultado}
        try:
            respuesta = requests.post(url = url, params = datos)
            respuesta.json()
            return True
        except:
            print("Error al comunicarse con el websocket")
            return False 