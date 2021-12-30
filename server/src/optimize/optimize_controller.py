from typing import List
from fastapi import APIRouter
from config.container import *
from dependency_injector.wiring import  inject

from config.shared import dependency
from src.optimize.usecase.optimize_path_service import OptimizePathService
from src.plotter.domain.project import OptimizationMethod

router = APIRouter(
    prefix="/optimize",
    tags=["optimize"],
    responses={404: {"description": "Not found"}},
)


#@router.get("/")
#@inject
#async def get_plotters(repository: PlotterRepository = dependency(Container.plotter.plotter_repository)):
#    return repository.getAll()

@router.post("/optimize/project/actual")
@inject
async def optimize_project(service: OptimizePathService = dependency(Container.optimize.optimize_path_service)):
    await service.optimize_command_group_path(OptimizationMethod.TabuSearch)
