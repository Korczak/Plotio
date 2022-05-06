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
        b64 = urlsafe_b64decode(str(arg1.content)); 
        npimg = np.fromstring(b64, dtype=np.uint8); 
        img = cv2.imdecode(npimg, 0)
        threshold = 128
        
        ret, thresh_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        
        object_color = 0
        all_commands: List[Command] = []
        for x in range(0, img.shape[0]):
            if x % 2 == 0:
                for y in range(0, img.shape[1]):
                    if(thresh_img[x, y] == object_color):
                        all_commands.append(Command(PlotterPosition(y, x, 1)))
            else:
                for y in range(img.shape[1] - 1, 0, -1):
                    if(thresh_img[x, y] == object_color):
                        all_commands.append(Command(PlotterPosition(y, x, 1)))
  
        print(all_commands[9060].command_detail.posX)
        print(all_commands[9060].command_detail.posY)
        currPos = PlotterPosition(0, 0, 0)
        totalDistance = 0    
        for com in all_commands:
            dist = max(abs(currPos.posX - com.command_detail.posX), abs(currPos.posY - com.command_detail.posY))
            currPos = com.command_detail
            totalDistance = totalDistance + dist

        print(f"TOTAL DISTANCE {totalDistance}")
        plotter = self.plotter_repository.get_plotter()
        plotter.add_project(Project(arg1.name, True, ProjectStatus.Ready, all_commands, all_commands, None, thresh_img, thresh_img, img.shape, totalDistance, 0))
        self.plotter_repository.update_plotter(plotter)
        optimize_project = OptimizeProject(arg1.name, all_commands, all_commands, thresh_img)
        pub.sendMessage(EventsName.ProjectAdded, arg1=optimize_project)
        