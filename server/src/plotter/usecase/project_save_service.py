import logging
from src.plotter.domain.project import Project
from src.plotter.infrastructure.plotter_repository import PlotterRepository
from src.plotter.infrastructure.project_repository import ProjectRepository
import json


class ProjectSaveService:
    def __init__(self, plotter_repository : PlotterRepository, project_repository: ProjectRepository) -> None:
        self.plotter_repository: PlotterRepository = plotter_repository
        self.project_repository : ProjectRepository = project_repository
        
    def save_project(self):
        active_project = self.project_repository.get_active_project();
        logging.debug(f'Zapisano projekt')
        if(active_project != None):
            active_project.save_to_file()
        
    def restore_project_from_file(self):
        with open("aktualny_project.json", "r") as reader:
            content = reader.read()
            project_dict = json.loads(content)
        plotter = self.plotter_repository.get_plotter()
        plotter.restore_project(project_dict['commands_done'])
        self.plotter_repository.update_plotter(plotter)
