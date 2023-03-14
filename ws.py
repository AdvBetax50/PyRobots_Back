from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.dictidPartidaIdsClientes = {}

    async def connect(self, websocket: WebSocket,partida_id:int,cliente_id:int):
        await websocket.accept()
        if not partida_id in self.dictidPartidaIdsClientes:    
            self.dictidPartidaIdsClientes[partida_id] = {}
        self.dictidPartidaIdsClientes[partida_id][cliente_id] = websocket
            
    def disconnect(self, websocket: WebSocket, partida_id, cliente_id):
        del( self.dictidPartidaIdsClientes[partida_id][cliente_id] )
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcastUnidos(self, partida, unidos):
        for part_id in self.dictidPartidaIdsClientes:
            for cliente in self.dictidPartidaIdsClientes[part_id]:
                await self.dictidPartidaIdsClientes[part_id][cliente].send_json(
                    {"partidas":partida, "unidos":unidos})
    
    async def broadcastResultados(self, partida, resltados):
        try:
            for cliente in self.dictidPartidaIdsClientes[partida]:
                await self.dictidPartidaIdsClientes[partida][cliente].send_json(
                    {"partida":partida, "terminado": resltados})
        except:
            print("Partida fuera de rango")
            pass

manager = ConnectionManager()

@app.websocket("/ws/unirse/{partida_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, partida_id: int, client_id: int):
    await manager.connect(websocket, partida_id, client_id)
    try:
        while True:
            await websocket.receive_text()
            await manager.send_personal_message("conectado"  , websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, partida_id, client_id)

@app.post("/ws/cantidad/")
async def ws_cantidad_unidos(partida:int, unidos: int):
    await manager.broadcastUnidos(partida, unidos)
    return {'exito': True}

@app.post("/ws/resultado/")
async def ws_resultados_partida(partida:int, resultado:bool):
    await manager.broadcastResultados(partida, resultado)
    return {'exito': True}