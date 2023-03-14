from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.RegistrarUsuario import RegistrarUsuario

IUT = RegistrarUsuario('example.sqlite')

usuario_con_avatar = {
    "nombre":"Admin", 
    "correo":"borderlanderspyrobots@gmail.com",  
    "contrasena":"aaaa-AAAA1", 
    "avatar":"imagen"}

usuario_sin_avatar = {
    "nombre":"Admin", 
    "correo":"borderlanderspyrobots@gmail.com",  
    "contrasena":"aaaa-AAAA1",
    "avatar":None}

class TestMockValue(TestCase):

    # Admin ya existe en la base de datos.
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_existe_nombre(self, mock_response):
        mock_response.return_value = True
        response = IUT.registrarUsuario(usuario_con_avatar)
        self.assertEqual(response, {"result":"NOMBRE_INVALIDO"})
    
    # El correo admin@admin.com ya existe en la base de datos.
    @mock.patch("fun.Sesion.SesionDB.existeCorreoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_existe_correo(self,mock_nombre, mock_correo):
        mock_nombre.return_value = False
        mock_correo.return_value = True
        response = IUT.registrarUsuario(usuario_con_avatar)
        self.assertEqual(response, {"result":"CORREO_INVALIDO"})

    # La contraseña no es valida
    @mock.patch("fun.RegistrarUsuario.RegistrarUsuario.validarContrasena")
    @mock.patch("fun.Sesion.SesionDB.existeCorreoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_contraseña_invalida(self,mock_nombre, mock_correo, mock_contrasena):
        mock_nombre.return_value = False
        mock_correo.return_value = False
        mock_contrasena.return_value = False
        response = IUT.registrarUsuario(usuario_con_avatar)
        self.assertEqual(response, {"result":"CONTRASENA_INVALIDA"})

    # El registro se usuario sin avatar se realiza con exito.
    @mock.patch("smtplib.SMTP_SSL")
    @mock.patch("fun.Sesion.SesionDB.registrarRobotSinAvatar")
    @mock.patch("fun.Sesion.SesionDB.registrarUsuarioSinAvatar")
    @mock.patch("fun.Sesion.SesionDB.existeCorreoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_registro_exitoso_sin_avatar(self, mock_nombre, mock_correo, mock_registro,
            mock_robot, _):
        mock_nombre.return_value = False
        mock_correo.return_value = False
        mock_registro.return_value = True
        mock_robot.return_value = 1
        response = IUT.registrarUsuario(usuario_sin_avatar)
        self.assertEqual(response, {"result":"USUARIO_REGISTRADO"})

    # El registro se usuario con avatar se realiza con exito.
    @mock.patch("smtplib.SMTP_SSL")
    @mock.patch("fun.Sesion.SesionDB.registrarRobotSinAvatar")
    @mock.patch("fun.Sesion.SesionDB.registrarUsuarioConAvatar")
    @mock.patch("fun.Sesion.SesionDB.existeCorreoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_registro_exitoso_con_avatar(self, mock_nombre, mock_correo, mock_registro,
            mock_robot,_):
        mock_nombre.return_value = False
        mock_correo.return_value = False
        mock_registro.return_value = True
        mock_robot.return_value = 1
        response = IUT.registrarUsuario(usuario_con_avatar)
        self.assertEqual(response, {"result":"USUARIO_REGISTRADO"})