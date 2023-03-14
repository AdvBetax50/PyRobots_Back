from unittest import TestCase, mock
import base64

import sys
sys.path.append("..")
from fun.Login import CheckLogIng

IUT = CheckLogIng('example.sqlite')

class TestMockValue(TestCase):

    # Usuario Incorrecto
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_incorrecto(self, mock_nombre):
        mock_nombre.return_value = False
        response = IUT.loginShowUsuarios({"nombre":"Admin","contrasena": "aaaa-AAAA1"})
        self.assertEqual(response["result"], "El usuario no existe en la base de datos")

    # Usuario no verificado
    @mock.patch("fun.Sesion.SesionDB.esValidoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_no_valido(self, mock_nombre, mock_valido):
        mock_nombre.return_value = True
        mock_valido.return_value = False
        response = IUT.loginShowUsuarios({"nombre":"Admin","contrasena": "aaaa-AAAA1"})
        self.assertEqual(response["result"], "El usuario no esta verificado")

    # Usuario Correcto
    @mock.patch("fun.Sesion.SesionDB.existeUsuarioContrasena")
    @mock.patch("fun.Sesion.SesionDB.esValidoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_usuario_correcto(self, mock_nombre, mock_valido, mock_contrasena):
        mock_nombre.return_value = True
        mock_valido.return_value = True
        mock_contrasena.return_value = True
        response = IUT.loginShowUsuarios({"nombre":"Admin","contrasena": "aaaa-AAAA1"})
        self.assertEqual(response["result"], "El usuario existe y la contraseña es correcta")
    
    # Contraseña Incorrecta
    @mock.patch("fun.Sesion.SesionDB.existeUsuarioContrasena")
    @mock.patch("fun.Sesion.SesionDB.esValidoUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_contrasena_incorrecta(self, mock_nombre, mock_valido, mock_contrasena):
        mock_nombre.return_value = True
        mock_valido.return_value = True
        mock_contrasena.return_value = False
        response = IUT.loginShowUsuarios({"nombre":"Admin","contrasena": "aaaa-AAAA1"})
        self.assertEqual(response["result"], "El usuario existe pero la contraseña es incorrecta")

    # Test Avatar
    @mock.patch("fun.Sesion.SesionDB.obtenerAvatarUsuarioDB")
    def test_usuario_avatar(self, mock_avatar):
        mock_avatar.return_value = base64.b64encode(b"avatar")
        response = IUT.obtenerAvatarUsuario("nombre")
        self.assertEqual(response, base64.b64encode(b"avatar"))