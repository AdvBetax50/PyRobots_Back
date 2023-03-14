from pony.orm import db_session, select, delete
from bd.entities import define_database_and_entities

class SesionDB:

    def __init__(self, db_name):
        self.db = define_database_and_entities(
            provider='sqlite', filename=db_name, create_db=True)

#========== USUARIO ==========

    @db_session
    def registrarUsuarioSinAvatar(self, us_dic):
        usuario = self.db.Usuario(
            nombre = us_dic["nombre"], 
            correo = us_dic["correo"], 
            contrasena = us_dic["contrasena"], 
            verificado = False)
        usuario.flush()
        return usuario.id

    @db_session
    def registrarUsuarioConAvatar(self,us_dic):
        usuario = self.db.Usuario(
            nombre = us_dic["nombre"], 
            correo = us_dic["correo"], 
            contrasena = us_dic["contrasena"],
            avatar = us_dic["avatar"], 
            verificado = False)
        usuario.flush()
        return usuario.id

    @db_session
    def existeNombreUsuario(self, nombre_usuario):
        return self.db.Usuario.exists(nombre = nombre_usuario)

    @db_session
    def existeCorreoUsuario(self,correo_usuario):
        return self.db.Usuario.exists(correo = correo_usuario)

    @db_session
    def obtenerIdUsuario(self,nombre_usuario):
        usuario = self.db.Usuario.get(nombre=nombre_usuario)
        return usuario.id

    @db_session
    def validarUsuario(self, nombre_usuario):
        usuario = self.db.Usuario.get(nombre=nombre_usuario)
        usuario.verificado = True

    @db_session
    def esValidoUsuario(self, nombre_usuario):
        usuario = self.db.Usuario.get(nombre=nombre_usuario)
        return usuario.verificado
    
    @db_session
    def existeUsuarioContrasena(self, nombre_usuario, contrasena_usuario):
        return self.db.Usuario.exists(
            lambda p: p.nombre == nombre_usuario and 
            p.contrasena == contrasena_usuario)

    @db_session
    def obtenerAvatarUsuarioDB(self, nombre_usuario):
       usuario = self.db.Usuario.get(nombre=nombre_usuario)
       return usuario.avatar

#========== ROBOT ==========

    @db_session
    def registrarRobotSinAvatar(self, robot):
        robot_nuevo = self.db.Robot(
            nombre = robot.get("nombre_robot"), 
            codigo = robot.get("codigo"),
            usuario = self.db.Usuario.get(id=robot.get("id_usuario"))
        )
        robot_nuevo.flush()
        return robot_nuevo.id

    @db_session
    def registrarRobotConAvatar(self, robot):
        robot_nuevo = self.db.Robot(
            nombre = robot.get("nombre_robot"), 
            avatar = robot.get("avatar"),
            codigo = robot.get("codigo"),
            usuario = self.db.Usuario.get(id=robot.get("id_usuario"))
        )
        robot_nuevo.flush()
        return robot_nuevo.id

    @db_session
    def obtenerAvatarRobotDB(self, id_robot):
       robot = self.db.Robot.get(id = id_robot)
       return robot.avatar
    
    @db_session
    def existeRobotUsuario(self, nombre_us, robot_id):
       usuario = self.db.Usuario.get(nombre = nombre_us)
       return robot_id in usuario.robots.id
    
    @db_session
    def stringRobot(self,id_Robot):
        robotBd = self.db.Robot.get(id = id_Robot)
        return robotBd.codigo
    
    @db_session
    def listarRobotDB(self, nombre_us):
        partidas_list = []
        robot_db = select(
            rob for rob in self.db.Robot 
                if rob.usuario.nombre == nombre_us)
        for rob in robot_db:
            dic = dict(
                id = rob.id,
                nombre = rob.nombre)
            partidas_list.append(dic)
        return partidas_list
 
#========== PARTIDA ==========

    @db_session
    def registrarPartidaCreadaDB(self, partida_dic):
        partidaNueva = self.db.Partida(
            nombre = partida_dic["nombre"],
            contrasena = partida_dic["contrasena"],
            jugadoresMax = partida_dic["jugadoresMax"],
            jugadoresMin = partida_dic["jugadoresMin"],
            juegosTotales = partida_dic["juegosTotales"],
            rondasTotales = partida_dic["rondasTotales"],
            usuarioCreador = self.db.Usuario.get(nombre=partida_dic["nombreUsuario"]),
            robotsUnidos = self.db.Robot.get(id=partida_dic["robotUsuario"]),
            estado = "DISPONIBLE")
        partidaNueva.flush()
        return partidaNueva.id

    @db_session
    def registrarUsuarioEnPartida(self, datos):
        partida = self.db.Partida.get(id=datos["partida_id"])
        usuario = self.db.Usuario.get(nombre=datos["nombre_us"])
        robot = self.db.Robot.get(id=datos["robot_id"])
        partida.usuariosUnidos.add(usuario)
        partida.robotsUnidos.add(robot)
        return True
    
    @db_session
    def borrarUsuarioDePartida(self, datos):
        partida = self.db.Partida.get(id=datos["partida_id"])
        robot_id = 0
        for r in partida.robotsUnidos:
            if r.usuario.nombre == datos["nombre_us"]:
                robot_id = r.id
        usuario = self.db.Usuario.get(nombre=datos["nombre_us"])
        robot = self.db.Robot.get(id=robot_id)
        partida.usuariosUnidos.remove(usuario)
        partida.robotsUnidos.remove(robot)
        return True

    @db_session
    def obtenerResultadosPartida(self, partida_id):
        partida = self.db.Partida.get(id=partida_id)
        resultados= []
        for res in partida.resultados:
            resultado_robot = {
                "robotId": res.robot.id,
                "robotNombre":res.robot.nombre,
                "resultado": res.robotResultado,
                "ganados": res.juegosGanados,
                "perdidos": res.juegosPerdidos,
                "empatados": res.juegosEmpatados
            }
            resultados.append(resultado_robot)
        return resultados

    @db_session
    def existePartida(self, partida_id):
        return self.db.Partida.exists(id = partida_id)
    
    @db_session
    def terminarPartida(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        partida.estado = "TERMINADO"
        return True

    @db_session
    def estaTerminadaPartida(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        return partida.estado == "TERMINADO"

    @db_session
    def consultarCantidadUnidos(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        return len(partida.usuariosUnidos) + 1
    
    @db_session
    def consultarCreadorPartida(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        return partida.usuarioCreador.nombre
    
    @db_session
    def esCreadorPartida(self, partida_id, nombre_us):
        partida = self.db.Partida.get(id = partida_id)
        return partida.usuarioCreador.nombre == nombre_us
 
    @db_session
    def estaLlenaPartida(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        return partida.jugadoresMax <= len(partida.usuariosUnidos)+1

    @db_session
    def esCantidadUsValida(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        cantUnidos = len(partida.usuariosUnidos)+1
        return (partida.jugadoresMin <= cantUnidos 
                and cantUnidos <= partida.jugadoresMax)

    @db_session
    def tieneContrasena(self, partida_id):
        partida = self.db.Partida.get(id = partida_id)
        return not partida.contrasena == ''
    
    @db_session
    def esCorrectaContrasena(self, partida_id, contrasena):
        partida = self.db.Partida.get(id = partida_id)
        return partida.contrasena == contrasena
    
    @db_session
    def estaUnido(self, partida_id, nombre_us):
        partida = self.db.Partida.get(id = partida_id)
        esta_unido = partida.usuarioCreador.nombre == nombre_us 
        if (not esta_unido):
            for u in partida.usuariosUnidos:
                esta_unido = esta_unido or u.nombre == nombre_us
        return esta_unido
    
    @db_session
    def listarPartidasDB(self, nombre_us):
        partidas_list = []
        partidas_bd = select(
            p for p in self.db.Partida )
        for p in partidas_bd:
            dic = dict(
                id = p.id,
                nombre = p.nombre,
                jugadoresMax = p.jugadoresMax,
                jugadoresMin = p.jugadoresMin,
                juegosTotales = p.juegosTotales, 
                rondasTotales = p.rondasTotales,
                terminado = p.estado == "TERMINADO")
            partidas_list.append(dic)
        return partidas_list

    @db_session
    def obtenerDatosPartidas(self,partida_id):
        partida_db = self.db.Partida.get(id = partida_id)
        robots_unidos = []
        for robot in partida_db.robotsUnidos:
            robots_unidos.append(robot.id)
        dic_partida = dict(
            rondas = partida_db.rondasTotales,
            juegos = partida_db.juegosTotales,
            robots = robots_unidos)
        return dic_partida

#========== RESULTADOS ==========
    @db_session
    def registrarResultados(self,lista_res_dic):
        list_id = []
        for res_dic in lista_res_dic:
            resultado = self.db.Resultado(
                robot = res_dic["robot"],
                partida = res_dic["partida"],
                robotResultado =res_dic["robot_resultado"],
                juegosGanados = res_dic["juegos_ganados"],
                juegosPerdidos = res_dic["juegos_perdidos"],
                juegosEmpatados = res_dic["juegos_empatados"]
            )
            resultado.flush()
            list_id.append(resultado.id)
        return list_id
        

#========== DB ==========

    def eliminarTodasLasTablas(self):
        self.db.drop_all_tables(with_all_data=True)
        self.db.create_tables()