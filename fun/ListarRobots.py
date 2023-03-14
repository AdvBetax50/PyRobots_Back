import sys
sys.path.append("..")
from fun.Sesion import SesionDB

class ListarRobots:

    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
    
    def obtenerAvatarRobot(self, id_robot):
        return self.db.obtenerAvatarRobotDB(id_robot)

    def listarRobots(self, nombre_us):
        respuesta = []
        if self.db.existeNombreUsuario(nombre_us):
            respuesta = self.db.listarRobotDB(nombre_us)
        return respuesta
