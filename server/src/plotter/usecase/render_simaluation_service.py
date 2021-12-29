import cv2
import numpy as np
import base64
from typing import List
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from pydantic import BaseModel

from src.plotter.infrastructure.project_repository import ProjectRepository


class PlotterPosition(BaseModel):
    positionX: int
    positionY: int

class RenderSimulationService:
    def __init__(self, plotter_repository: PlotterRepository, project_repository: ProjectRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository
        self.project_repository: ProjectRepository = project_repository

    def get_actual_position(self):
        plotter = self.plotter_repository.get_plotter()
        return PlotterPosition(positionX=plotter.position.posX, positionY=plotter.position.posY)

    def get_all_commands(self) -> List[PlotterPosition]:
        project = self.project_repository.get_active_project()
        
        return [PlotterPosition(positionX = command.command_detail.posX, positionY = command.command_detail.posY) for command in project.all_commands]

    def get_image_with_processed_commands(self) -> str:
        project = self.project_repository.get_active_project()
        if(project is None):
            return None

        _, im_arr = cv2.imencode('.jpg', project.image_with_processed_commands)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)


        return im_b64

    def get_original_image(self) -> str:
        project = self.project_repository.get_active_project()
        if(project is None):
            return None

        _, im_arr = cv2.imencode('.jpg', project.image_content)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)


        return im_b64

