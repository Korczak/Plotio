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
        equivalency_list, labels, num_of_commands = self.extract_sub_images(img, thresh_img, object_color)
        
        commandGroups: List[CommandGroup] = []
        
        unique_labels = list(set(equivalency_list.values()))
                
            
        if num_of_commands > 50000:
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
            
        else:
            for label in unique_labels:
                commandGroups.append(CommandGroup([]))
            for x in range(0, img.shape[0]):
                for y in range(0, img.shape[1]):
                    if(labels[x, y] != 0):
                        commandGroups[unique_labels.index(labels[x, y])].commands.append(Command(PlotterPosition(y, x, 1)))
                        
            #commandGroups.append(CommandGroup([Command(PlotterPosition(0, 0, 0))]))     
            all_commands: List[Command] = []
            for commandGroup in commandGroups:
                all_commands = all_commands + commandGroup.commands        
            
        plotter = self.plotter_repository.get_plotter()
        plotter.add_project(Project(arg1.name, True, ProjectStatus.Ready, all_commands, all_commands, thresh_img, thresh_img, img.shape))
        self.plotter_repository.update_plotter(plotter)            
        optimize_project = OptimizeProject(arg1.name, all_commands, all_commands, thresh_img, labels, unique_labels, commandGroups)
        pub.sendMessage(EventsName.ProjectAdded, arg1=optimize_project)
        
    def extract_sub_images(self, img: np.ndarray, thresh_img: np.ndarray, object_color: int):
        labels = np.zeros((img.shape[0], img.shape[1]))
        num_of_commands = 0
        
        curr_obj = 0
        equivalency_list = {}
        pixel_above, pixel_left = 0, 0
        
        
        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
                if(thresh_img[x, y] == object_color):
                    pixel_above, pixel_left = 0, 0
                    
                    if y > 0:
                        if labels[x][y-1] > 0:
                            pixel_above = equivalency_list[labels[x][y-1]]
                    
                    if x > 0:
                        if labels[x-1][y] > 0:
                            pixel_left = equivalency_list[labels[x-1][y]]
                        
                    if pixel_above != 0 and pixel_left != 0:
                        classification = min(pixel_above, pixel_left)
                        equivalency_list[pixel_left] = classification
                        equivalency_list[pixel_above] = classification
                    elif pixel_above != 0:
                        classification = pixel_above
                    elif pixel_left != 0:
                        classification = pixel_left
                    else:
                        curr_obj += 1 
                        equivalency_list[curr_obj] = curr_obj
                        classification = curr_obj
                      
                    labels[x][y] = int(classification)

        for x in range(0, img.shape[0]):
            for y in range(0, img.shape[1]):
                if(thresh_img[x][y] == object_color):
                    labels[x][y] = equivalency_list[int(labels[x][y])]
                    num_of_commands = num_of_commands + 1
        return equivalency_list, labels, num_of_commands
