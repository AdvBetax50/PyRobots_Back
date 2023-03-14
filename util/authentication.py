from fastapi import FastAPI, HTTPException, Header
from util.TokenManager import *

def get_usuario(token: str = Header(default=None)):
    tokenManager = TokenManager()
    infoToken = tokenManager.decodificar(token)
    if infoToken is None or infoToken["usuario"] is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    else: return infoToken["usuario"]
