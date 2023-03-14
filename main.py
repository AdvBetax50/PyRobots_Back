from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from pydantic import BaseModel, EmailStr
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Depends, File, Form, Response

from fun.Login import CheckLogIng
from fun.RegistrarRobot import RegistrarRobot
from fun.RegistrarUsuario import RegistrarUsuario
from fun.ValidarUsuario import  ValidarUsuario
from fun.ListarPartidas import ListarPartidas
from fun.ListarRobots import ListarRobots
from fun.Simulacion import Simulacion
from fun.RegistrarPartidaCreada import RegistrarPartida
from fun.UnirsePartida import UnirsePartida
from fun.AbandonarPartida import AbandonarPartida
from fun.IniciarPartida import PartidaIniciar
from fun.ResultadosPartida import ResultadosPartida

from util.authentication import *

app = FastAPI()

db_nombre = 'example.sqlite'

origins = [
    "http://front",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#===================== Metodos Get =============================

@app.get("/")
async def root():
    return {"message": "PyRobot"}


@app.get("/usuario/validar/{token}", response_class=HTMLResponse)
async def rootUsuarioValidar(nombre_us: str = Depends(get_usuario)):
    valUsuario = ValidarUsuario(db_nombre)
    return valUsuario.validarUsuario(nombre_us)

@app.get("/robot/listar/")
async def rootRobotListar(nombre_us: str = Depends(get_usuario)):
    listRob = ListarRobots(db_nombre)
    robot_dic = listRob.listarRobots(nombre_us)
    list_robot = []
    for rob in robot_dic:
        info_rob = dict(
            id = rob.get('id'),
            nombre = rob.get('nombre'))
        list_robot.append(info_rob)
    return list_robot

class Partida(BaseModel):
    id: int 
    nombre: str 
    jugadoresMax: int
    jugadoresMin: int
    juegosTotales: int
    rondasTotales: int
    usuariosUnidos: int
    creador: str
    terminado: bool
    contrasena: bool
    estaUnido: bool

class ListaDePartidas(BaseModel):
    lista: List[Partida]

@app.get("/partida/listar/", response_model=ListaDePartidas)
async def rootPartidaListar(nombre_us: str = Depends(get_usuario)):
    partidas = ListarPartidas(db_nombre)
    lista_dic = partidas.listarPartidasDisponibles(nombre_us)

    lista_partidas = []
    for dic in lista_dic:
        partida = Partida(
            id = dic.get('id'),
            nombre = dic.get('nombre'),
            jugadoresMax = dic.get('jugadoresMax'),
            jugadoresMin = dic.get('jugadoresMin'),
            juegosTotales = dic.get('juegosTotales'), 
            rondasTotales = dic.get('rondasTotales'),
            usuariosUnidos = dic.get('usuariosUnidos'),
            creador = dic.get('creador'),
            terminado = dic.get('terminado'),
            contrasena = dic.get('contrasena'),
            estaUnido = dic.get('estaUnido'))
        lista_partidas.append(partida)
    return ListaDePartidas(lista = lista_partidas)

@app.get("/partida/resultado/{partidaId}")
async def rootPartidaResultado(
        partidaId: int,
        nombre_us: str = Depends(get_usuario)):
    info_dic = {
        "partida_id": partidaId,
        "nombre_us": nombre_us}
    resultadosPartida = ResultadosPartida(db_nombre)
    resultados = resultadosPartida.obtenerResultados(info_dic)
    return resultados

@app.get("/robot/avatar/obtener/{id_robot}")
async def rootRobotAvatarObtener(id_robot: int):
    listRob = ListarRobots(db_nombre)
    avatar_robot = listRob.obtenerAvatarRobot(id_robot)
    return Response(content=avatar_robot, media_type="image/png")

@app.get("/usuario/avatar/obtener/")
async def rootUsuarioAvatarObtener(nombre_us: str = Depends(get_usuario)):
    login = CheckLogIng(db_nombre)
    avatar_usuario = login.obtenerAvatarUsuario(nombre_us)
    return Response(content=avatar_usuario, media_type="image/png")

#===================== Metodos Post =============================

@app.post("/partida/crear/")
async def rootPartidaCrear( 
        nombre: str = Form(),
        contrasena: str = Form(),
        jugadoresMax: int = Form(),
        jugadoresMin: int = Form(),
        juegosTotales: int = Form(),
        rondasTotales: int = Form(),
        robotUsuario: int = Form(),
        nombreUsuario: str = Depends(get_usuario)):
    partida_dic = { 
        "nombre": nombre,
        "contrasena": contrasena,
        "jugadoresMax": jugadoresMax,
        "jugadoresMin": jugadoresMin,
        "juegosTotales": juegosTotales,
        "rondasTotales": rondasTotales,
        "robotUsuario": robotUsuario,
        "nombreUsuario": nombreUsuario}
    registrarPartida = RegistrarPartida(db_nombre)
    msg = registrarPartida.registrarPartidaCreada(partida_dic)   
    return msg

@app.post("/partida/unirse/")
async def rootPartidaUnirse(
        partidaId: int = Form(),
        contrasena: str = Form(),
        robotUsuario: int = Form(), 
        nombre: str = Depends(get_usuario)):
    info_dic ={
        "nombre_us": nombre,
        "contrasena": contrasena,
        "partida_id": partidaId, 
        "robot_id": robotUsuario}
    unirsePartida = UnirsePartida(db_nombre)
    return unirsePartida.unirNuevoUsuario(info_dic)

@app.post("/partida/abandonar/")
async def rootPartidaAbandonar(
        partidaId: int = Form(), 
        nombre: str = Depends(get_usuario)):
    info_dic ={
        "nombre_us": nombre,
        "partida_id": partidaId}
    abandonarPartida = AbandonarPartida(db_nombre)
    return abandonarPartida.quitarUsuarioDePartida(info_dic)

@app.post("/partida/iniciar/")
async def rootPartidaIniciar(
        partidaId: int = Form(),
        nombre_us: str = Depends(get_usuario)):
    info_dic={
        "nombre_us":nombre_us,
        "partida_id":partidaId,
    }
    partidaIniciar = PartidaIniciar(db_nombre)
    respuesta = partidaIniciar.iniciarPartida(info_dic)
    return respuesta

@app.post("/usuario/iniciarsesion/")
async def rootBD(nombre: str = Form(), contrasena: str = Form(),):
    infoUsuario_dic ={
        "nombre":nombre, 
        "contrasena":contrasena}
    logIn_usuario = CheckLogIng(db_nombre)
    return logIn_usuario.loginShowUsuarios(infoUsuario_dic)

@app.post("/usuario/registrar/")
async def rootUsuarioRegistrar(
        avatar: Union[bytes, None] = File(default=None),
        nombre: str = Form(),
        contrasena: str = Form(),
        correo: EmailStr = Form() ):
    us_dic = {
        "avatar": avatar,
        "nombre": nombre,
        "contrasena": contrasena,
        "correo": correo}
    registrarUs = RegistrarUsuario(db_nombre)
    return registrarUs.registrarUsuario( us_dic)

@app.post("/robot/registrar/")
async def rootRobotRegistrar(
        avatar: Union[bytes, None] = File(default=None),
        nombre_usuario: str = Depends(get_usuario),
        nombre: str = Form(),
        codigo: str = Form()):
    regRobot = RegistrarRobot(db_nombre)
    robot = {
        "nombre_usuario":nombre_usuario, 
        "nombre":nombre, 
        "avatar":avatar, 
        "codigo":codigo}
    msg = regRobot.registrarRobot(robot)
    return msg
    

#------------------------------------- simulacion ---------------------------

class Misiles(BaseModel):
    pos_x:int
    pos_y:int
    orientacion:int
    explotado : bool

class PosicionesRobot(BaseModel):
    posicion:int
    id:int

class RobotJuego(BaseModel):
    id: int 
    nombre: str 
    pos_x: int
    pos_y: int
    velocidad: int
    estado: int
    vision: int
    canon: int

class RondasJuego(BaseModel):
    robots: List[RobotJuego] #lista de 2 a 4
    misiles: List[Misiles]
    
class SimulacionOut(BaseModel):
    simulacion: List[RondasJuego] # lista de 1 a 10 000
    posiciones: List[PosicionesRobot]

class SimulacionIn(BaseModel):
    usuario: str
    rondas: int
    robots: List[int]

@app.post("/simulacion/ejecutar/")
async def rootSimulacionEjecutar(simulacion_in: SimulacionIn, nombre_us: str = Depends(get_usuario)):
    simulacion = Simulacion()

    configuracion = dict(
        rondas = simulacion_in.rondas,
        robots = simulacion_in.robots
    )

    resultados_simulacion = simulacion.ejecutarSimulacion(configuracion, nombre_us)

    simulacion_out = SimulacionOut(simulacion=[],posiciones=[])
    for ronda in resultados_simulacion["simulacion"]:                               #list simulacion  
        ronda_juego = RondasJuego(robots=[],misiles=[])
        for robot in ronda["robots"]:                                               #list info de los robot por ronda
            robot_juego = RobotJuego(
                id = robot.get('id'),
                nombre = robot.get('nombre'),
                pos_x = robot.get('pos_x'),
                pos_y = robot.get('pos_y'),
                velocidad = robot.get('velocidad'),
                estado = robot.get('estado'),
                vision =robot.get('vision'),
                canon = robot.get('canon'))
            ronda_juego.robots.append(robot_juego)
        for misil in ronda["misiles"]:                                              #list info de los misiles por ronda
            misil_juedo = Misiles(
                    pos_x = misil.get('pos_x'),
                    pos_y = misil.get('pos_y'),
                    orientacion = misil.get('orientacion'),
                    explotado = misil.get('explotado')
            )
            ronda_juego.misiles.append(misil_juedo)
            
        simulacion_out.simulacion.append(ronda_juego)
        
    for pos_robot in resultados_simulacion["resultado"]:                            #list de las posiciones 
        robot_posicion = PosicionesRobot(
            id = pos_robot.get('id'),
            posicion= pos_robot.get('posicion')
           ) 
        simulacion_out.posiciones.append(robot_posicion)                  
        
    return {"resultados":simulacion_out}
