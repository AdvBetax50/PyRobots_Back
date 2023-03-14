import sys
sys.path.append("..")
from fun.Sesion import SesionDB

class ListarPartidas:
    
    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
        
    def listarPartidasDisponibles(self, nombre_us):
        partidas = self.db.listarPartidasDB(nombre_us)
        lista_dic = []
        for p in partidas:
            dic = dict(
                id = p.get('id'),
                nombre = p.get('nombre'),
                jugadoresMax = p.get('jugadoresMax'),
                jugadoresMin = p.get('jugadoresMin'),
                juegosTotales = p.get('juegosTotales'), 
                rondasTotales = p.get('rondasTotales'),
                terminado = p.get('terminado'),
                usuariosUnidos = self.db.consultarCantidadUnidos(p.get('id')),
                creador = self.db.consultarCreadorPartida(p.get('id')),
                contrasena = self.db.tieneContrasena(p.get('id')),
                estaUnido = self.db.estaUnido(p.get('id'), nombre_us))
            lista_dic.append(dic)
        return lista_dic
