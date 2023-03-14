import sys
sys.path.append("..")
from fun.Sesion import SesionDB

class ValidarUsuario:

    def __init__(self, db_nombre):
        self.db = SesionDB(db_nombre)
    
    def respuestaHTML(self, msg, link):
        return"""
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
        <img src="{linkPicture}" alt="Coche" style="width:10%" class="mx-auto d-block">
        <div style="height: 30px;"></div>
        <h1>{msg}</h1>
        <div style="height: 20px;"></div>
        <h4>¿Estas listo? Crea tu robot 🤖 y disfrutá de jugar con tus amigos</h4> 
        <div style="height: 40px;"></div>
        <a href="http://localhost:3000/iniciar-sesion">
            <button type="button" class="btn btn-success">Iniciar Sesion</button>
        </a>
    </div>

    </body>
    </html>
    """.format(linkPicture=link,msg=msg)

    def validarUsuario(self, usuario):
        respuesta=""
        if (self.db.existeNombreUsuario(usuario)):
            self.db.validarUsuario(usuario)
            respuesta = "Felicitaciones "+usuario+" su usuario esta verificado"
            link = "https://i.ibb.co/z5rb4rJ/accept.png"
        else:
            respuesta = "Lo sentimos "+usuario+" no se pudo verificar su usuario"
            link = "https://i.ibb.co/ZcDjFPV/eliminar.png"
        return self.respuestaHTML(respuesta,link) 
