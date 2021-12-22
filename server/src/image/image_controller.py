from typing import ContextManager
from fastapi import APIRouter, HTTPException, Depends
from fastapi_socketio import SocketManager
from config.container import *
from dependency_injector.wiring import Provide, inject

from config.shared import dependency
from src.image.usecase.add_image_service import AddImageInput, AddImageService

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)


#@router.get("/")
#@inject
#async def get_plotters(repository: PlotterRepository = dependency(Container.plotter.plotter_repository)):
#    return repository.getAll()

@router.post("/add-image")
@inject
async def add_image(input: AddImageInput, service: AddImageService = dependency(Container.image.add_image_service)):
    service.add_image(input)



# @socketio.event
# def my_event(message):
#     print('a')
#     emit('my_response', 'test')