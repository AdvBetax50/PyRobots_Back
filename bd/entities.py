from datetime import datetime
from pony.orm import *

def define_database_and_entities(**db_params):
    db = Database(**db_params)

    class Usuario(db.Entity):
        id = PrimaryKey(int, auto=True)
        nombre = Required(str)
        correo = Required(str)
        contrasena = Required(str)
        avatar = Optional(bytes)
        verificado = Required(bool)
        robots = Set('Robot')
        partidaCreador = Set('Partida', reverse='usuarioCreador')
        partidasUnidas = Set('Partida', reverse='usuariosUnidos')


    class Robot(db.Entity):
        id = PrimaryKey(int, auto=True)
        nombre = Required(str)
        avatar = Optional(bytes)
        codigo = Required(str)
        usuario = Required(Usuario)
        resultados = Set('Resultado')
        partidasUnidas = Set('Partida')


    class Partida(db.Entity):
        id = PrimaryKey(int, auto=True)
        nombre = Required(str)
        contrasena = Optional(str)
        estado = Required(str)
        jugadoresMax = Required(int)
        jugadoresMin = Required(int)
        juegosTotales = Required(int)
        rondasTotales = Required(int)
        usuarioCreador = Required(Usuario, reverse='partidaCreador')
        usuariosUnidos = Set(Usuario, reverse='partidasUnidas')
        robotsUnidos = Set(Robot)
        resultados = Set('Resultado')


    class Resultado(db.Entity):
        id = PrimaryKey(int, auto=True)
        robot = Required(Robot)
        partida = Required(Partida)
        robotResultado = Required(str)
        juegosGanados = Required(int)
        juegosPerdidos = Required(int)
        juegosEmpatados = Required(int)

    db.generate_mapping(create_tables=True)
    return db
