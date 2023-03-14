from dis import dis
from time import time
from typing import List

from fun.Rondas import *
from fun.RobotEnJuego import *
from fun.MisilDeRobot import *


class MisilDeRobot:
    def __init__(self, posx, posy, ang, distancia):
        self.posicion_misil = (posx, posy)
        self.orientacion = ang
        self.dist = distancia
        self.explotado = False
        
    def explosionMisil(self):
        self.explotado = True