from fun.Juego import Juego

class Simulacion:
    
    def ejecutarSimulacion(self, simulacion_confi, _):     #agregar chequeo que son los robots del usuario y que exista
        nuevoJuego = Juego()
        return nuevoJuego.iniciarJuego(simulacion_confi)
