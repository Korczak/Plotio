from enum import unique
from typing import List
import cv2
import numpy as np
from pubsub import pub
from base64 import urlsafe_b64decode, b64decode, b64encode
from src.events.events_name import EventsName
from src.optimize.domain.optimize_project import OptimizeProject
from src.plotter.domain.command import Command
from src.plotter.domain.command_group import CommandGroup
from src.plotter.domain.plotter_position import PlotterPosition
from src.plotter.domain.project import OptimizationMethod, Project, ProjectStatus
from src.plotter.infrastructure.plotter_repository import PlotterRepository

from src.plotter.infrastructure.project_repository import ProjectRepository
from src.events.image_added import ImageAdded

class ImageAdapter:
    def __init__(self, project_repository: ProjectRepository, plotter_repository: PlotterRepository) -> None:
        self.project_repository: ProjectRepository = project_repository
        self.plotter_repository: PlotterRepository = plotter_repository

    def subscribe(self):
        pub.subscribe(self.on_add_image, EventsName.ImageAdded)

    def on_add_image(self, arg1: ImageAdded):
        img = arg1.content
        
        max_color = 0;
        for x in range(0, img.shape[0]):    
            for y in range(0, img.shape[1]):
                max_color = max(max_color, img[x, y])
                
        all_commands: List[Command] = []
        for x in range(0, img.shape[0]):
            if x % 2 == 0:
                for y in range(0, img.shape[1]):
                    if(img[x, y] != max_color):
                        all_commands.append(Command(PlotterPosition(y, x, max_color - img[x, y])))
            else:
                for y in range(img.shape[1] - 1, 0, -1):
                    if(img[x, y] != max_color):
                        all_commands.append(Command(PlotterPosition(y, x, max_color - img[x, y])))
  
            
            
        plotter = self.plotter_repository.get_plotter()
        plotter.add_project(Project(arg1.name, True, ProjectStatus.Ready, all_commands, all_commands, img, img, img.shape))
        self.plotter_repository.update_plotter(plotter)            
        optimize_project = OptimizeProject(arg1.name, all_commands, all_commands, img)
        pub.sendMessage(EventsName.ProjectAdded, arg1=optimize_project)