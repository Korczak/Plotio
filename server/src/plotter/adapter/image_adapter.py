from typing import List
import cv2
import numpy as np
from pubsub import pub
from base64 import urlsafe_b64decode, b64decode, b64encode
from src.plotter.domain.command import Command
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.project import Project, ProjectStatus
from src.plotter.infrastructure.plotter_repository import PlotterRepository

from src.plotter.infrastructure.project_repository import ProjectRepository
from src.events.image_added import ImageAdded
from src.plotter.usecase.optimize_path_service import OptimizePathService

class ImageAdapter:
    def __init__(self, project_repository: ProjectRepository, plotter_repository: PlotterRepository, optimize_path_service: OptimizePathService) -> None:
        self.project_repository: ProjectRepository = project_repository
        self.plotter_repository: PlotterRepository = plotter_repository
        self.optimize_path_service: OptimizePathService = optimize_path_service

    def subscribe(self):
        pub.subscribe(self.on_add_image, 'ImageAdded')

    def on_add_image(self, arg1: ImageAdded):
        b64 = urlsafe_b64decode(str(arg1.content)); 
        npimg = np.fromstring(b64, dtype=np.uint8); 
        img = cv2.imdecode(npimg, 0)
        threshold = 128
        
        ret, thresh_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

        commands: List[Command] = []
        
        commands.append(Command(PlotterPosition(0, 0, 0)))

        for y in range(0, img.shape[1]):
            for x in range(0, img.shape[0]):
                if(thresh_img[x, y] == 0):
                    commands.append(Command(PlotterPosition(y, x, 1)))
                    
        commands.append(Command(PlotterPosition(0, 0, 0)))            
        
        plotter = self.plotter_repository.get_plotter()
        plotter.add_project(Project(arg1.name, True, ProjectStatus.NotStarted, commands, commands, thresh_img, img.shape))
        self.plotter_repository.update_plotter(plotter)
        
        self.optimize_path_service.optimize_path(plotter)
