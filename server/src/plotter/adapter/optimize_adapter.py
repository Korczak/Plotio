
from pubsub import pub
from src.events.events_name import EventsName
from src.events.project_optimalized import ProjectOptimized
from src.plotter.infrastructure.project_repository import ProjectRepository


class OptimizeAdapter:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self.project_repository: ProjectRepository = project_repository

    def subscribe(self):
        pub.subscribe(self.on_project_optimized, EventsName.ProjectOptimalized)
        
    def on_project_optimized(self, arg1: ProjectOptimized):
        project = self.project_repository.get_active_project()

        project.optimize_command_groups(arg1.optimized_commands)
        self.project_repository.update_project(project)