import jwt

class TokenManager():
    SECRET = "secret"
    ALGORITHMS = ["HS256"]

    def generar(self):
        pass

    def decodificar(self, token: str):
        try:
            return jwt.decode(token, self.SECRET, algorithms=self.ALGORITHMS)
        except:
            return None
