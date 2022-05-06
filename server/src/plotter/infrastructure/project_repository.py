
from typing import List

from numpy import ndarray
from src.plotter.domain.command import Command
from src.plotter.domain.project import Project, ProjectStatus
from src.plotter.infrastructure.project_dto import ProjectDto


class ProjectRepository:
    
    def __init__(self) -> None:
        #self._project_db: List[ProjectDto] = [] 
        self._active_project: ProjectDto = None

    def add_project(self, name: str, is_active: bool, status: ProjectStatus, commands: List[Command], previous_command: Command, image_content: ndarray, image_with_processed_commands: ndarray, image_shape: List[int], totalDistance: int, distanceCompleted: int) -> None:
        projectDto = ProjectDto(name, is_active, status, commands, commands, previous_command, image_content, image_with_processed_commands, image_shape, totalDistance, distanceCompleted)

        #self._project_db.append(projectDto)
        self._active_project = projectDto
        
    def add_project(self, project: Project) -> None:
        projectDto = ProjectDto(project.name, project.is_active, project.status, project.all_commands, project.commands_to_do, project.previous_command, project.image_content, project.image_with_processed_commands, project.image_shape, project.totalDistance, project.distanceCompleted)

        #self._project_db.append(projectDto)
        self._active_project = projectDto

    def update_project(self, project: Project):
        projectDto = ProjectDto(project.name, project.is_active, project.status, project.all_commands, project.commands_to_do, project.previous_command, project.image_content, project.image_with_processed_commands, project.image_shape, project.totalDistance, project.distanceCompleted)

        #self._project_db.append(projectDto)
        self._active_project = projectDto

    def get_active_project(self) -> Project:
        if(self._active_project is None):
            return None
        
        project = self._active_project
        
        return Project(project.name, project.is_active, project.status, project.all_commands, project.commands_to_do, project.previous_command, project.image_content, project.image_with_processed_commands, project.image_shape, project.totalDistance, project.distanceCompleted)