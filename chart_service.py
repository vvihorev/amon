from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import json

from fastapi import WebSocket


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConnectionManager(metaclass=Singleton):
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket
        await websocket.send_text(json.dumps({"type": "noop"}))

    async def disconnect(self, username: str):
        if username in self.active_connections:
            self.active_connections.pop(username)

    async def broadcast(self, data):
        for connection in self.active_connections.values():
            await connection.send_json(data)


templates = Jinja2Templates(directory="static")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(client_id)


@app.post("/chart")
async def post(request: Request):
    data = await request.json()
    await manager.broadcast(data)
    return {"result": "ok"}


@app.get("/", response_class=HTMLResponse)
async def get(
    request: Request,
):
    return templates.TemplateResponse(request=request, name="index.html", context={})

