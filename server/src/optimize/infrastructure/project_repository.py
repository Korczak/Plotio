
from typing import List

from src.optimize.infrastructure.project_dto import ProjectDto
from src.optimize.domain.optimize_project import OptimizeProject


class ProjectRepository:
    
    def __init__(self) -> None:
        self._project_db: List[ProjectDto] = [] 
        self._active_project: ProjectDto = None

    def add_project(self, project: OptimizeProject):
        projectDto = ProjectDto(project.name, project.all_commands, project.commands_to_do, project.image_content, project.labels, project.unique_labels, project.command_groups)

        self._project_db.append(projectDto)
        self._active_project = projectDto
        
    def update_project(self, project: OptimizeProject):
        projectDto = ProjectDto(project.name, project.all_commands, project.commands_to_do, project.image_content, project.labels, project.unique_labels, project.command_groups)

        self._project_db[-1] = projectDto
        self._active_project = projectDto

    def get_active_project(self) -> OptimizeProject:
        if(self._active_project is None):
            return None
        
        project = self._active_project
        
        return OptimizeProject(project.name, project.all_commands, project.commands_to_do, project.image_content)