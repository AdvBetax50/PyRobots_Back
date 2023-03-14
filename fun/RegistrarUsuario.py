import sys
sys.path.append("..")
from fun.Sesion import SesionDB
import jwt

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class RegistrarUsuario:
    
    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)

    def registrarUsuario(self, us_dic):
        respuesta = {"result":"USUARIO_REGISTRADO"}
        if (self.db.existeNombreUsuario(us_dic["nombre"])):
            respuesta = {"result":"NOMBRE_INVALIDO"}
        elif(self.db.existeCorreoUsuario(us_dic["correo"])):
            respuesta = {"result":"CORREO_INVALIDO"}
        elif(not self.validarContrasena(us_dic["contrasena"])):
            respuesta = {"result":"CONTRASENA_INVALIDA"}
        else:
            id_us = 0
            if(us_dic["avatar"] == None):
                id_us = self.db.registrarUsuarioSinAvatar(us_dic)
            else:
                id_us = self.db.registrarUsuarioConAvatar(us_dic)
            self.registrarRobotsEjemplo(id_us)
            self.enviarCorreoDeVerificacion(us_dic)
        return respuesta

    def validarContrasena(self, contrasena):
        return (
            len(contrasena) >= 8 and
            len(contrasena) <= 20 and
            not contrasena.islower() and 
            not contrasena.isupper() and 
            '-' in contrasena and
            any(chr.isdigit() for chr in contrasena))

    def registrarRobotsEjemplo(self, id_us):
        robot_1 = dict(
            id_usuario = id_us,
            nombre_robot = "Robot Ejemplo 1",
            codigo = self.getCodigoRobot1())
        self.db.registrarRobotSinAvatar(robot_1)
        robot_2 = dict(
            id_usuario = id_us,
            nombre_robot = "Robot Ejemplo 2",
            codigo = self.getCodigoRobot2())
        self.db.registrarRobotSinAvatar(robot_2) 

    def enviarCorreoDeVerificacion(self,us_dict):
        emailReceptor         = us_dict["correo"]
        emailEmisor           = "borderlandersPyrobots@gmail.com"
        contrasenaEmailEmisor = "btfzwezjsqqrwzzc" 
        asunto                = "Correo de verificación Pyrobots."
        cuerpo                = self.crearCuerpoCorreoVerificacion(
                                            us_dict["nombre"])

        mesage = MIMEMultipart()
        mesage["from"]    = emailEmisor
        mesage["to"]      = emailReceptor
        mesage["subject"] = asunto
        mesage.attach(MIMEText(cuerpo, "html"))
        
        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context = contexto) as smtp:
            smtp.login(emailEmisor, contrasenaEmailEmisor)
            smtp.sendmail(emailEmisor, emailReceptor, mesage.as_string())

    def crearCuerpoCorreoVerificacion(self,nombre_usuario):
        token = jwt.encode({"usuario": nombre_usuario}, "secret", algorithm="HS256")
        url = "http://127.0.0.1:8000/usuario/validar/" + token
        cuerpo="""
    <div>
        <h1>PyRobots</h1>
        <p>Hola {usuario}!. Para continuar con la verificación de su cuenta presione el siguiente link:</p>

        <a href="{url}">Validar cuenta</a>

        <p>Atte: Borderlanders Group.</p>
    </div>
        """.format(usuario=nombre_usuario, url=url)
        return cuerpo
    
    def getCodigoRobot1(self):
        return """
class SuperClase(Robot):
    def initialize(self):
        self.x = 0
        self.y = 0
        self.angulo_robot = 0
        self.angulo_canon = 0

    def responds(self):
        self.x , self.y = self.get_position()

        if (self.x -10 <= 0):
            self.angulo_robot = 0
            self.angulo_canon = 90
        elif (self.x + 10 >= 999):
            self.angulo_robot = 180
            self.angulo_canon = 270

        if (self.y - 10 <= 0):
            self.angulo_robot = 90
            self.angulo_canon = 180
        elif (self.y + 10 >= 999):
            self.angulo_robot = 270
            self.angulo_canon = 0

        if (self.angulo_robot >= 360): 
            self.angulo_robot = 0
        else:
            self.angulo_robot += 3
        self.drive(self.angulo_robot, 40)

        if (self.angulo_canon <= 0): 
            self.angulo_canon = 360
        else:
            self.angulo_canon -= 3
        self.cannon(self.angulo_canon, 500) 
"""

    def getCodigoRobot2(self):
        return """
class SuperClase(Robot):
    def initialize(self):
        self.x = 0
        self.y = 0
        self.angulo_robot = 0
        self.velocidad = 20

    def responds(self):
        self.x , self.y = self.get_position()
        self.point_scanner(self.angulo_robot, 15)
        scn = self.scanned()

        if (self.x -10 <= 0):
            self.angulo_robot = 0
        elif (self.x + 10 >= 999):
            self.angulo_robot = 180
  
        if (self.y - 10 <= 0):
            self.angulo_robot = 90
        elif (self.y + 10 >= 999):
            self.angulo_robot = 270

        if (self.angulo_robot <= 0): 
            self.angulo_robot = 360
        else:
            if (scn==0 and self.velocidad > 0):
                self.angulo_robot -= 5
            elif(scn>0 and scn-100 < 0):
                self.velocidad = 0
            else:
                self.velocidad = 20
        
        self.drive(self.angulo_robot, self.velocidad)

        distancia = 100
        if (scn > 0):
            distancia = scn

        self.cannon(self.angulo_robot, distancia) 
"""