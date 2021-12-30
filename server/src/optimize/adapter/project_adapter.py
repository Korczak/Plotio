
from pubsub import pub
from src.optimize.domain.optimize_project import OptimizeProject
from src.optimize.infrastructure.project_repository import ProjectRepository


class ProjectAdapter:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self.project_repository: ProjectRepository = project_repository

    def subscribe(self):
        pub.subscribe(self.on_project_added, 'ProjectAdded')

    def on_project_added(self, arg1: OptimizeProject):        
        
        self.project_repository.add_project(arg1)