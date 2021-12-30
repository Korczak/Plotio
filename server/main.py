from dependency_injector import providers
from dependency_injector.wiring import Provide
import uvicorn
import logging
from logging import config, debug
from typing import Iterator, List
from fastapi import Depends, FastAPI, HTTPException, status, BackgroundTasks
from fastapi_socketio import SocketManager
from fastapi.middleware.cors import CORSMiddleware
from src.image import image_controller
from src.optimize import optimize_controller

from src.plotter import plotter_controller
from src.plotter.module import PlotterModule
from config.container import Container
import asyncio

print(__name__)

logger = logging.getLogger(__name__)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "localhost:8080",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

container = Container()
container.optimize.project_adapter().subscribe()
container.plotter.plotter_position_service().subscribe()
container.plotter.optimize_adapter().subscribe()
container.plotter.image_adapter().subscribe()
container.plotter.alarm_service().subscribe()
container.plotter.alert_service().subscribe()

container.wire(modules=[__name__, image_controller, plotter_controller, optimize_controller])
app.container = container


socket_manager = SocketManager(app=app, cors_allowed_origins=[], mount_location='/ws', socketio_path='/socket.io', async_mode="asgi")

app.include_router(plotter_controller.router)
app.include_router(image_controller.router)
app.include_router(optimize_controller.router)

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(container.plotter.automatic_command_service().send_to_controller())
    asyncio.create_task(container.plotter.automatic_command_service().receive_from_controller())
    pass
    
@app.get("/")
async def root():
    global socket_manager
    await socket_manager.emit('PlotterPositionChanged', 'new position')
    await socket_manager.send('new position')
    #await socket_manager.emit('message', 'new position')
    return {"message": "Hello Bigger Applications!"}

@app.sio.on("PlotterPositionChanged")
def onPlotter(arg):
    print("Received event plotter")

# @app.sio.on("connect")
# def onConnect(arg):
#     print("Received event plotter")

@app.sio.on("message")
def onMessage(arg):
    print("Received event plotter")



