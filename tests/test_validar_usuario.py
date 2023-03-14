from unittest import TestCase, mock

import sys
sys.path.append("..")
from fun.ValidarUsuario import ValidarUsuario

IUT = ValidarUsuario('example.sqlite')

class TestMockValue(TestCase): 
   
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_validacion_fallida(self, mock_usuario):
        mock_usuario.return_value = False
        response = IUT.validarUsuario("Admin")
        self.assertEqual(response,"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Bootstrap Example</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body style="height: 100%;">

    <div class="jumbotron text-center">
        <img src="https://i.ibb.co/ZcDjFPV/eliminar.png" alt="Coche" style="width:10%" class="mx-auto d-block">
        <div style="height: 30px;"></div>
        <h1>Lo sentimos Admin no se pudo verificar su usuario</h1>
        <div style="height: 20px;"></div>
        <h4>¿Estas listo? Crea tu robot 🤖 y disfrutá de jugar con tus amigos</h4> 
        <div style="height: 40px;"></div>
        <a href="http://localhost:3000/iniciar-sesion">
            <button type="button" class="btn btn-success">Iniciar Sesion</button>
        </a>
    </div>

    </body>
    </html>
    """)

    @mock.patch("fun.Sesion.SesionDB.validarUsuario")
    @mock.patch("fun.Sesion.SesionDB.existeNombreUsuario")
    def test_validacion_exitosa(self, mock_usuario,mock_validar):
        mock_usuario.return_value = True
        response = IUT.validarUsuario("Admin")
        self.assertEqual(response,"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>Bootstrap Example</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body style="height: 100%;">

    <div class="jumbotron text-center">
        <img src="https://i.ibb.co/z5rb4rJ/accept.png" alt="Coche" style="width:10%" class="mx-auto d-block">
        <div style="height: 30px;"></div>
        <h1>Felicitaciones Admin su usuario esta verificado</h1>
        <div style="height: 20px;"></div>
        <h4>¿Estas listo? Crea tu robot 🤖 y disfrutá de jugar con tus amigos</h4> 
        <div style="height: 40px;"></div>
        <a href="http://localhost:3000/iniciar-sesion">
            <button type="button" class="btn btn-success">Iniciar Sesion</button>
        </a>
    </div>

    </body>
    </html>
    """)