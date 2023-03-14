import base64
import pytest

import sys
sys.path.append("..")
from fun.Sesion import SesionDB

nombre_db_test = 'test.sqlite'

@pytest.fixture()
def obtener_avatar():
    return base64.b64encode(b"avatar")

@pytest.fixture()
def codigo_de_robot():
#"class SuperRobot:\n\tdef initialize():\n\t\tpass\n\n\tdef responds():\n\t\tpass"
    return """\
class SuperRobot:\
    def initialize():\
        pass\
    def responds():\
        pass\
"""

@pytest.fixture()
def usuario_sin_avatar():
    return {
        "nombre": "Admin1", 
        "correo": "Admin@admin", 
        "contrasena": "Admin-01"}
    
@pytest.fixture()
def usuario_con_avatar(obtener_avatar):
    return {
        "nombre": "Admin2", 
        "correo": "Admin@admin", 
        "contrasena": "Admin-01",
        "avatar": obtener_avatar}

@pytest.fixture()
def robot_sin_avatar(codigo_de_robot):
    return {
        "nombre_robot": "robot_sin_avatar", 
        "codigo":codigo_de_robot,
        "id_usuario":1}

@pytest.fixture()
def robot_con_avatar(codigo_de_robot, obtener_avatar):
    return {
        "nombre_robot": "robot_con_avatar", 
        "codigo":codigo_de_robot,
        "id_usuario":2,
        "avatar": obtener_avatar}

@pytest.fixture()
def partida_sin_contrasena():
    return {
        "nombre":"par_sin_contrasena",
        "contrasena":"",
        "jugadoresMax":2,
        "jugadoresMin":2,
        "juegosTotales":100,
        "rondasTotales":200,
        "robotUsuario":1,
        "nombreUsuario":"Admin1"}

@pytest.fixture()
def partida_con_contrasena():
    return {
        "nombre":"par_con_contrasena",
        "contrasena":"contrasena",
        "jugadoresMax":3,
        "jugadoresMin":3,
        "juegosTotales":100,
        "rondasTotales":200,
        "robotUsuario":2,
        "nombreUsuario":"Admin2"}

@pytest.fixture()
def resultado_robot_sin_avatar():
    return {
        "robot":1,
        "partida":1,
        "robot_resultado":"Ganador",
        "juegos_ganados":50,
        "juegos_perdidos":40,
        "juegos_empatados":10}

class TestValue():

    def test_registrar_usario_sin_avatar(self, usuario_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        response = db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        assert(response == 1)
    
    def test_registrar_usario_con_avatar(self, usuario_con_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        response = db.registrarUsuarioConAvatar(usuario_con_avatar)
        assert(response == 1)
   
    def test_existe_usuario(self, usuario_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        response = db.existeNombreUsuario("admin1")
        assert(response == False)
        response = db.existeNombreUsuario("Admin1")
        assert(response == True)
        response = db.existeCorreoUsuario("admin@admin")
        assert(response == False)
        response = db.existeCorreoUsuario("Admin@admin")
        assert(response == True)
        response = db.existeUsuarioContrasena("Admin1", "admin@admin")
        assert(response == False) 
        response = db.existeUsuarioContrasena("Admin1", "Admin-01")
        assert(response == True)
    
    def test_obtener_id(self, usuario_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        id_us = db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        response = db.obtenerIdUsuario("Admin1") 
        assert(response == id_us)
   
    def test_validar_usuario(self, usuario_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)        
        db.validarUsuario("Admin1")
        response = db.esValidoUsuario("Admin1")
        assert(response == True)
    
    def test_avatar_usuario(self,
            usuario_con_avatar,
            obtener_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioConAvatar(usuario_con_avatar)
        response = db.obtenerAvatarUsuarioDB("Admin2")
        assert(response == obtener_avatar)
    
    def test_registrar_robot_sin_avatar(self,
            usuario_sin_avatar,
            robot_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        response = db.registrarRobotSinAvatar(robot_sin_avatar) 
        assert(response == 1)
    
    def test_registrar_robot_con_avatar(self,
            usuario_sin_avatar,
            usuario_con_avatar,
            robot_con_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarUsuarioConAvatar(usuario_con_avatar)
        response = db.registrarRobotConAvatar(robot_con_avatar) 
        assert(response == 1)
    
    def test_existe_robot(self, usuario_sin_avatar, robot_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        id_robot = db.registrarRobotSinAvatar(robot_sin_avatar)
        response = db.existeRobotUsuario("Admin1", id_robot)
        assert(response == True)
    
    def test_avatar_robot(self,
            usuario_sin_avatar,
            robot_con_avatar,
            obtener_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        robot_id = db.registrarRobotConAvatar(robot_con_avatar)
        response = db.obtenerAvatarRobotDB(robot_id)
        assert(response == obtener_avatar)

    def test_codigo_robot(self,
            usuario_sin_avatar, 
            robot_sin_avatar,
            codigo_de_robot):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        robot_id = db.registrarRobotSinAvatar(robot_sin_avatar)
        response = db.stringRobot(robot_id)
        assert(response == codigo_de_robot)

    def test_listar_robot(self,
            usuario_sin_avatar, 
            robot_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        robot1_id = db.registrarRobotSinAvatar(robot_sin_avatar)
        robot2_id = db.registrarRobotConAvatar(robot_sin_avatar)
        response = db.listarRobotDB("Admin1")
        assert(response == [{
            "id":robot1_id,
            "nombre":"robot_sin_avatar"},{
            "id":robot2_id,
            "nombre":"robot_sin_avatar"
            }])

    def test_registrar_partida(self,
            usuario_sin_avatar,
            robot_sin_avatar,
            partida_sin_contrasena):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarRobotSinAvatar(robot_sin_avatar)
        partida_id = db.registrarPartidaCreadaDB(partida_sin_contrasena)
        assert(partida_id == 1)
        response = db.existePartida(partida_id)
        assert(response == True)
        response = db.esCreadorPartida(partida_id,"Admin1")
        assert(response == True)
        response = db.esCreadorPartida(partida_id,"Admin2")
        assert(response == False)
        response = db.obtenerDatosPartidas(partida_id)
        assert(response == {
            "rondas":200,
            "juegos":100,
            "robots":[1]})
    
    def test_unir_y_abandonar_partida(self,
            usuario_sin_avatar,
            usuario_con_avatar,
            robot_sin_avatar,
            robot_con_avatar,
            partida_sin_contrasena):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarUsuarioSinAvatar(usuario_con_avatar)
        db.registrarRobotSinAvatar(robot_sin_avatar)
        db.registrarRobotSinAvatar(robot_con_avatar)
        partida_id = db.registrarPartidaCreadaDB(partida_sin_contrasena)
        respuesta = db.estaLlenaPartida(partida_id)
        assert(respuesta == False)
        respuesta = db.esCantidadUsValida(partida_id)
        assert(respuesta == False)
        db.registrarUsuarioEnPartida({
            "partida_id":1,
            "nombre_us":"Admin2",
            "robot_id":2})
        assert(db.estaUnido(partida_id, "Admin2"))
        respuesta = db.estaLlenaPartida(partida_id)
        assert(respuesta == True)
        respuesta = db.esCantidadUsValida(partida_id)
        assert(respuesta == True)
        db.borrarUsuarioDePartida({
            "partida_id":1,
            "nombre_us":"Admin2"})
        assert(not db.estaUnido(partida_id, "Admin2"))

    def test_listar_partida(self,
            usuario_sin_avatar,
            usuario_con_avatar,
            robot_sin_avatar,
            robot_con_avatar,
            partida_sin_contrasena,
            partida_con_contrasena):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarUsuarioConAvatar(usuario_con_avatar)
        db.registrarRobotSinAvatar(robot_sin_avatar)
        db.registrarRobotConAvatar(robot_con_avatar)
        id_partida1 = db.registrarPartidaCreadaDB(partida_sin_contrasena)
        id_partida2 = db.registrarPartidaCreadaDB(partida_con_contrasena)
        response = db.listarPartidasDB("Admin1")
        assert(response == [{
            "id":id_partida1,
            "nombre":"par_sin_contrasena",
            "jugadoresMax":2,
            "jugadoresMin":2,
            "juegosTotales":100,
            "rondasTotales":200,
            'terminado': False},{
            "id":id_partida2,
            "nombre":"par_con_contrasena",
            "jugadoresMax":3,
            "jugadoresMin":3,
            "juegosTotales":100,
            "rondasTotales":200,
            'terminado': False}])
        response = db.consultarCreadorPartida(id_partida1)
        assert(response == "Admin1")
        response = db.estaUnido(id_partida1, "Admin1")
        assert(response == True)
        response = db.estaUnido(id_partida1, "Admin2")
        assert(response == False)
        response = db.tieneContrasena(id_partida1)
        assert(response == False)
        response = db.tieneContrasena(id_partida2)
        assert(response == True)
        response = db.esCorrectaContrasena(id_partida1, "contrasena")
        assert(response == False)
        response = db.esCorrectaContrasena(id_partida2, "contrasena")
        assert(response == True)

    def test_resultados(self,
            usuario_sin_avatar,
            robot_sin_avatar,
            partida_sin_contrasena,
            resultado_robot_sin_avatar):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarRobotSinAvatar(robot_sin_avatar)
        partida_id = db.registrarPartidaCreadaDB(partida_sin_contrasena)
        db.registrarResultados([resultado_robot_sin_avatar])
        db.terminarPartida(partida_id)
        response = db.estaTerminadaPartida(partida_id)
        assert(response == True)
        response = db.obtenerResultadosPartida(partida_id)
        assert(response == [{
                "robotId":1,
                "robotNombre":"robot_sin_avatar",
                "resultado":"Ganador",
                "ganados": 50,
                "perdidos": 40,
                "empatados": 10}])

    def test_consultar_unidos_partida(self,
            usuario_sin_avatar,
            robot_sin_avatar,
            partida_sin_contrasena):
        db = SesionDB(nombre_db_test)
        db.eliminarTodasLasTablas()
        db.registrarUsuarioSinAvatar(usuario_sin_avatar)
        db.registrarRobotSinAvatar(robot_sin_avatar)
        id_partida = db.registrarPartidaCreadaDB(partida_sin_contrasena)
        response = db.consultarCantidadUnidos(id_partida)
        assert(response == 1)