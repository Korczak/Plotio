from typing import ContextManager
from fastapi import APIRouter, HTTPException, Depends
from fastapi_socketio import SocketManager
from config.container import *
from dependency_injector.wiring import Provide, inject

from config.shared import dependency
from src.image.usecase.add_image_service import AddImageInput, AddImageService
from src.image.usecase.edit_image_service import EditImageService, ImageAttributeInput
from src.image.usecase.image_preview_service import ImagePreviewService

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
    
@router.post("/edit-image")
@inject
async def edit_image(input: ImageAttributeInput, service: EditImageService = dependency(Container.image.edit_image_service)):
    service.edit_image_attributes(input)

@router.post("/approve-image")
@inject
async def approve_image(service: EditImageService = dependency(Container.image.edit_image_service)):
    service.approve_image()

@router.get("/preview")
@inject
async def get_image_preview(service: ImagePreviewService = dependency(Container.image.image_preview_service)):
    image_str = service.get_image()
    return image_str


# @socketio.event
# def my_event(message):
#     print('a')
#     emit('my_response', 'test')