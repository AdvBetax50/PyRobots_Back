from operator import imod
from pony.orm import *
import base64

import sys
sys.path.append("..")
from fun.Sesion import SesionDB

class RegistrarRobot:

    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)

    def registrarRobotNuevo(self, ro_dic):
        id_robot = None
        if (ro_dic["avatar"] == None):
            registro = dict(
                id_usuario = self.db.obtenerIdUsuario(ro_dic["nombre_usuario"]),
                nombre_usuario = ro_dic["nombre_usuario"],
                nombre_robot = ro_dic["nombre"],
                codigo = ro_dic["codigo"])
            id_robot = self.db.registrarRobotSinAvatar(registro)
        else:
            registro = dict(
            id_usuario = self.db.obtenerIdUsuario(ro_dic["nombre_usuario"]),
                nombre_usuario = ro_dic["nombre_usuario"],
                nombre_robot = ro_dic["nombre"],
                avatar = ro_dic["avatar"],
                codigo = ro_dic["codigo"])
            id_robot = self.db.registrarRobotConAvatar(registro)
        return id_robot

    def registrarRobot(self, ro_dic):
        respuesta = {}
        if(not self.db.existeNombreUsuario(ro_dic["nombre_usuario"])):
            respuesta = {"result":"Usuario_No_Registrado"}
        else: 
            id = self.registrarRobotNuevo(ro_dic)
            respuesta = {"id":id}
        return respuesta
